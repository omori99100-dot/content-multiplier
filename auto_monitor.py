import subprocess
import time

# أمر تشغيل التطبيق
APP_COMMAND = ["streamlit", "run", "streamlit_app.py"]

def run_and_monitor():
    print("🚀 جاري تشغيل التطبيق (وضع المراقبة الخفيف)...")
    
    while True:
        process = subprocess.Popen(
            APP_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        error_log = ""
        error_detected = False

        # قراءة الأخطاء لحظة بلحظة
        for line in process.stderr:
            print(line, end="")
            
            if any(keyword in line for keyword in ["Traceback", "Error:", "Exception:", "ImportError"]):
                error_detected = True
            
            if error_detected:
                error_log += line

        process.wait()

        # إذا انهار التطبيق وظهر خطأ
        if error_detected and error_log.strip():
            print("\n" + "="*50)
            print("⚠️ تم اكتشاف خطأ أدى لانهيار التطبيق!")
            print("="*50)
            print(error_log)
            print("="*50)
            
            print("⏳ التطبيق متوقف. قم بإصلاح الخطأ وحفظ الملف...")
            print("🔄 سيتم إعادة تشغيل التطبيق تلقائياً بعد 10 ثوانٍ.\n")
            time.sleep(10)
        else:
            print("✅ التطبيق يعمل بشكل سليم أو تم إيقافه يدوياً.")
            break

if __name__ == "__main__":
    run_and_monitor()
