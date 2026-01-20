import redis
import json
import time
from PIL import Image
import os
import socket

REDIS_HOST = "192.168.1.111"  # Nahraď IP adresou master nodu
INPUT_FOLDER = '/shared/images/input'
OUTPUT_FOLDER = '/shared/images/output'

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
worker_id = socket.gethostname()

def process_image(filename):
    """Převede obrázek na černobílý"""
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    
    img = Image.open(input_path)
    bw_img = img.convert('L')  # L = černobílý režim
    bw_img.save(output_path)
    
    return True

def worker_loop():
    print(f"🚀 Worker {worker_id} started")
    
    # Registrace workera
    r.setex(f'worker:{worker_id}', 30, time.time())
    
    while True:
        try:
            # Heartbeat - worker je aktivní
            r.setex(f'worker:{worker_id}', 30, time.time())
            
            # Získej úlohu z fronty (blocking s timeoutem)
            task_data = r.brpop('image_queue', timeout=5)
            
            if task_data:
                task = json.loads(task_data[1])
                filename = task['filename']
                
                print(f"📸 Processing: {filename}")
                
                # Označ jako zpracovávající se
                r.hset(f'image:{filename}', 'status', 'processing')
                r.hset(f'image:{filename}', 'worker', worker_id)
                
                start_time = time.time()
                
                try:
                    # Zpracuj obrázek
                    process_image(filename)
                    
                    processing_time = time.time() - start_time
                    
                    # Označ jako hotové
                    r.hset(f'image:{filename}', 'status', 'completed')
                    r.hset(f'image:{filename}', 'processing_time', processing_time)
                    
                    print(f"✅ Completed: {filename} in {processing_time:.2f}s")
                    
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")
                    # Vrať zpět do fronty při chybě
                    r.lpush('image_queue', json.dumps(task))
                    r.hset(f'image:{filename}', 'status', 'pending')
            
        except KeyboardInterrupt:
            print(f"👋 Worker {worker_id} shutting down")
            r.delete(f'worker:{worker_id}')
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

if __name__ == '__main__':
    worker_loop()
