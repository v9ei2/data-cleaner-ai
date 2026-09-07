import argparse
import sys


def configure_stdout():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")


def build_prompts(topic, use_case):
    prompt_1 = f"""أنت محلل بيانات أول {use_case}. مهمتك {topic} لدعم قرارات الإدارة، وليس لعرض إحصائيات فقط.

السياق:
- الموضوع: {topic}
- حالة الاستخدام: {use_case}
- الجمهور: الإدارة التنفيذية ومدراء الأقسام (غير تقنيين).
- القيود: لا تفترض بيانات غير موجودة. إذا نقصت معلومة، اذكرها كـ "فرضية" أو "سؤال يحتاج بيانات".

المطلوب منك:
1) حدّد الأسئلة التجارية الصحيحة قبل التحليل (5–8 أسئلة).
2) اقترح الحد الأدنى من البيانات المطلوبة لكل سؤال (جداول/حقول/فترة زمنية).
3) ضع خطة تحليل من 4 مراحل: تنظيف، استكشاف، تحليل سببي/مقارن، توصيات.
4) لكل مرحلة: المخرجات المتوقعة + مقاييس الجودة (مثل نسبة القيم الناقصة، ثبات الاتجاه، حجم العينة).
5) اختم بـ 3 توصيات قابلة للتنفيذ خلال 30 يوماً، كل توصية بصيغة: المشكلة → الدليل → الإجراء → الأثر المتوقع → المالك المقترح.

صيغة الرد:
- لغة عربية واضحة
- جداول مختصرة
- لا كلام عام بدون معيار قياس"""

    prompt_2 = f"""أريد منك إعداد تقرير تنفيذي عن {topic} {use_case}. اعتبر نفسك مستشار قرارات، لا باحث أكاديمي.

الموضوع: {topic}
حالة الاستخدام: {use_case}

افترض توفر بيانات تشغيلية ومالية ومبيعات للـ 12 شهراً الماضية. قبل التحليل، اسأل فقط عن:
- نوع النشاط
- أهم KPI الحالي
- القرار المطلوب هذا الشهر

بعد الإجابة، قدّم تقريراً بهذا الهيكل الثابت:
A. الخلاصة التنفيذية (8 أسطر كحد أقصى)
B. ما الذي تغيّر؟ (الاتجاهات، الانحرافات، الموسمية)
C. أين نخسر أو نكسب القيمة؟ (حسب المنتج/القناة/العميل/الفريق إن أمكن)
D. المخاطر الخفية (جودة البيانات، تحيز العينة، مؤشرات مضللة)
E. 3 سيناريوهات قرار:
   - محافظ
   - متوازن
   - هجومي
   لكل سيناريو: التكلفة، الأثر، مؤشرات المتابعة، شرط التوقف
F. لوحة متابعة أسبوعية: 6 مؤشرات فقط مع تعريف كل مؤشر وطريقة حسابه وعتبة التنبيه

قواعد صارمة:
- كل رقم يجب أن يرتبط بقرار.
- فرّق بين الارتباط والسببية.
- إذا كانت البيانات غير كافية، قل "لا يكفي للحسم" بدلاً من التخمين."""

    prompt_3 = f"""صمم بروتوكول معياري لـ {topic} {use_case} يمكن لأي محلل جديد تطبيقه خلال أسبوع، بدون الاعتماد على خبرة فردية.

الموضوع: {topic}
حالة الاستخدام: {use_case}

المطلوب تسليمه كـ Playbook عملي:

1) Data Intake
- قائمة تحقق لاستلام الملفات (CSV/Excel/SQL)
- معايير قبول/رفض الملف
- تعريف المفاتيح الأساسية (Customer ID, Order ID, Date, Amount...)

2) Cleaning Standard
- قواعد موحدة للتعامل مع: القيم الناقصة، التواريخ، العملات، التكرارات، القيم الشاذة
- متى نحذف صفاً؟ متى نُصححه؟ متى نُعلّمه فقط؟
- سجل تدقيق (Audit log) يوثّق كل تغيير

3) Analysis Cookbook
- 8 تحليلات جاهزة مرتبطة بـ {topic} {use_case}:
  1. نمو الإيرادات
  2. تركز العملاء
  3. جودة القنوات
  4. كفاءة التشغيل
  5. التسرب/churn إن وجد
  6. الموسمية
  7. الربحية حسب الشريحة
  8. إنذارات مبكرة
- لكل تحليل: الهدف، الخطوات، المقياس، الرسم البياني المناسب، خطأ شائع يجب تجنبه

4) Decision Pack
قالب صفحة واحدة يذهب للإدارة كل أسبوع:
- ماذا لاحظنا
- لماذا يهم
- ماذا نفعل
- كيف نقيس النجاح خلال 14 يوماً

أضف في النهاية: نسخة "Prompt داخلي" قصيرة يستخدمها الفريق مع ChatGPT/Claude عند كل تحليل جديد، مع أماكن واضحة لملء: مصدر البيانات، الفترة، السؤال التجاري، والقرار المطلوب."""

    return [
        {
            "title": "Prompt 1: محلل بيانات (professional)",
            "why": "يحدد الدور والجمهور والقيود، ويطلب أسئلة تجارية ثم بيانات ثم خطة ثم توصيات قابلة للتنفيذ.",
            "prompt": prompt_1,
        },
        {
            "title": "Prompt 2: تقرير تنفيذي (actionable)",
            "why": "يربط التحليل بقرار حقيقي عبر سيناريوهات وعتبات تنبيه، ويمنع التخمين عندما لا تكفي البيانات.",
            "prompt": prompt_2,
        },
        {
            "title": "Prompt 3: بروتوكول معياري (repeatable)",
            "why": "يحوّل التحليل إلى نظام داخلي قابل للتكرار: استلام، تنظيف، وصفات تحليل، وقالب قرار أسبوعي.",
            "prompt": prompt_3,
        },
    ]


def print_output(topic, use_case, prompts):
    print("User Input:")
    print(f'- Topic: "{topic}"')
    print(f'- Use Case: "{use_case}"')
    print()
    print("Script Output:")
    for item in prompts:
        print(f"- {item['title']}")
    print()
    for item in prompts:
        print("=" * 72)
        print(item["title"])
        print("-" * 72)
        print("Why it's good:")
        print(item["why"])
        print()
        print(item["prompt"])
        print()


def parse_args():
    parser = argparse.ArgumentParser(description="Generate 3 professional ChatGPT/Claude prompts.")
    parser.add_argument("--topic", default="", help='Topic, e.g. "تحليل بيانات"')
    parser.add_argument("--use-case", dest="use_case", default="", help='Use case, e.g. "للشركة"')
    return parser.parse_args()


def main():
    configure_stdout()
    args = parse_args()
    topic = args.topic.strip()
    use_case = args.use_case.strip()
    if not topic:
        topic = input("Topic [تحليل بيانات]: ").strip() or "تحليل بيانات"
    if not use_case:
        use_case = input("Use Case [للشركة]: ").strip() or "للشركة"
    prompts = build_prompts(topic, use_case)
    print()
    print_output(topic, use_case, prompts)


if __name__ == "__main__":
    main()
