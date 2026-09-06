# استيراد مكتبة Anthropic للاتصال بـ Claude API
import os
# استيراد مكتبة csv لحفظ الملف الناتج بشكل صحيح
import csv
# استيراد io لقراءة نص CSV القادم من Claude كملف في الذاكرة
import io
# استيراد Anthropic client
from anthropic import Anthropic


# اسم الموديل المستخدم لتنظيف البيانات
MODEL = "claude-sonnet-4-20250514"
# الأعمدة الافتراضية للناتج
DEFAULT_COLUMNS = "name, age, department, location"


def read_input_file(path):
    # فتح ملف النص للقراءة
    with open(path, "r", encoding="utf-8") as file:
        # قراءة كل المحتوى كسلسلة نصية واحدة
        return file.read()


def build_prompt(raw_text, columns):
    # تعليمات واضحة لـ Claude: يخرج CSV فقط بدون شرح
    return (
        "You are a careful data-cleaning assistant.\n"
        "Task: clean and structure the messy text into CSV format.\n"
        f"Columns (in this exact order): {columns}\n"
        "Rules:\n"
        "- Output ONLY valid CSV. No markdown. No explanation. No extra text.\n"
        "- First row must be the header using the given column names.\n"
        "- One person/record per row.\n"
        "- Trim extra spaces and fix obvious typos when the meaning is clear.\n"
        "- If a value is missing, leave that cell empty.\n"
        "- Do not invent names, ages, departments, or locations that are not in the text.\n"
        "- Age must be a number when present.\n"
        "\n"
        "Messy data:\n"
        f"{raw_text}\n"
    )


def clean_with_claude(raw_text, columns, api_key):
    # إنشاء عميل Anthropic باستخدام مفتاح الـ API
    client = Anthropic(api_key=api_key)
    # بناء الـ prompt حسب الأعمدة والبيانات الخام
    prompt = build_prompt(raw_text, columns)
    # إرسال الطلب إلى Claude
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    # أخذ النص من أول جزء في الرد
    return response.content[0].text.strip()


def save_csv(csv_text, output_path):
    # قراءة نص CSV في الذاكرة للتحقق أنه صالح
    reader = csv.reader(io.StringIO(csv_text))
    # تحويل كل الصفوف إلى قائمة
    rows = list(reader)
    # فتح ملف الإخراج للكتابة
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        # إنشاء كاتب CSV
        writer = csv.writer(file)
        # كتابة كل الصفوف إلى الملف
        writer.writerows(rows)
    # إرجاع الصفوف للاستخدام في الطباعة
    return rows


def main():
    # طلب مسار ملف الإدخال من المستخدم
    input_path = input("Input file path [input.txt]: ").strip() or "input.txt"
    # طلب مسار ملف الإخراج من المستخدم
    output_path = input("Output CSV path [output.csv]: ").strip() or "output.csv"
    # طلب أسماء الأعمدة أو استخدام الافتراضي
    columns = input(f"CSV columns [{DEFAULT_COLUMNS}]: ").strip() or DEFAULT_COLUMNS
    # قراءة مفتاح API من متغير البيئة
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    # إذا لم يكن المفتاح في البيئة، اطلبه من المستخدم بدون تخزين دائم
    if not api_key:
        api_key = input("ANTHROPIC_API_KEY: ").strip()
    # التوقف إذا لم يوجد مفتاح
    if not api_key:
        raise SystemExit("Missing ANTHROPIC_API_KEY.")
    # قراءة البيانات العشوائية/الفوضوية من الملف
    raw_text = read_input_file(input_path)
    # التوقف إذا كان الملف فارغ
    if not raw_text.strip():
        raise SystemExit("Input file is empty.")
    # تنظيف البيانات عبر Claude
    csv_text = clean_with_claude(raw_text, columns, api_key)
    # حفظ الناتج في ملف CSV
    rows = save_csv(csv_text, output_path)
    # طباعة الناتج في التيرمنال
    print("\n--- Cleaned CSV ---")
    # طباعة كل صف مفصول بفاصلة
    for row in rows:
        print(",".join(row))
    # تأكيد مسار الملف المحفوظ
    print(f"\nSaved to {output_path}")


# تشغيل البرنامج فقط عند استدعائه مباشرة
if __name__ == "__main__":
    main()
