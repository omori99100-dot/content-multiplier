import subprocess
import time
import interpreter
import sys

# 1. إعدادات النظام
interpreter.auto_run = True
APP_COMMAND = ["streamlit", "run", "streamlit_app.py"]
MAX_RETRIES = 3  # الحد الأقصى لمحاولات الإصلاح المتتالية

def backup_with_git():
    """حفظ حالة الكود الحالية في Git قبل أن يقوم الذكاء الاصطناعي بتعديله"""
    print("📦 جاري حفظ نسخة احتياطية (Git Commit) قبل بدء الإصلاح الآلي...")
    try:
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", "Auto-backup before AI applies fixes"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ تم حفظ الكود بنجاح في Git!")
    except subprocess.CalledProcessError:
        print("ℹ️ لم يتم العثور على تعديلات جديدة لحفظها في Git.")

def fix_error_with_ai(error_log: str):
    """توجيه Open Interpreter بصلاحيات كاملة لتعديل الملفات وتثبيت المكتبات"""
    prompt = f"""
    The application crashed. You have full permission to fix it automatically.
    
    Tasks:
    1. Read the necessary local Python files to understand the context.
    2. Modifying Codes: Rewrite or edit the Python files directly to fix code errors.
    3. Installing Packages: Run terminal commands (like `uv pip install` or `pip install`) to install missing dependencies.
    
    Do not ask for confirmation, just write the code/commands and run them to fix the issue.
    
    ERROR LOG:
    {error_log}
    """
    
    try:
        interpreter.chat(prompt)
        print("\n🔧 تم تطبيق التعديلات! جاري إعادة تشغيل التطبيق بعد 3 ثوانٍ...\n")
        time.sleep(3)
    except Exception as e:
        print(f"❌ فشل الإصلاح الآلي: {e}")
        sys.exit(1)

def run_and_monitor():
    """تشغيل التطبيق ومراقبته باستمرار مع حد أقصى للمحاولات"""
    print("🚀 جاري تشغيل التطبيق وبدء المراقبة الآلية...")
    retries = 0
    
    while retries < MAX_RETRIES:
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

        # معالجة الخطأ
        if error_detected and error_log.strip():
            retries += 1
            print(f"\n⚠️ تم اكتشاف خطأ! (المحاولة {retries} من {MAX_RETRIES})")
            
            # الإيقاف الآمن عند تجاوز الحد
            if retries >= MAX_RETRIES:
                print("🛑 تم الوصول للحد الأقصى من المحاولات الآلية. النظام يحتاج إلى تدخل بشري!")
                break
                
            backup_with_git() 
            print("🤖 تسليم المهمة لـ Open Interpreter للتحليل والتعديل...\n")
            
            # استدعاء دالة الإصلاح
            fix_error_with_ai(error_log)
        else:
            print("✅ التطبيق يعمل بشكل سليم أو تم إيقافه يدوياً.")
            break

if __name__ == "__main__":
    run_and_monitor()
