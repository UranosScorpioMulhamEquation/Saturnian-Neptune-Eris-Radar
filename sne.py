import flet as ft
import uuid
import os
import traceback
from datetime import datetime

# تحديد مجلد التطبيق لضمان صلاحيات القراءة والكتابة على الأندرويد
APP_DIR = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()
KEY_FILE = os.path.join(APP_DIR, "license.key")
ID_FILE = os.path.join(APP_DIR, "device_id.txt")

# ==================== 1. Core Mathematics Logic ====================
def run_combined_matrix_engine(birth_date):
    # معاملات معادلة نبتون وهوميا وإيريس
    homo_k, eris_k, neptune_k, tolerance = 6.18, 9.3, 10.77, 0.3
    results = []
    
    # فحص السنوات العمرية من 1 إلى 90 عاماً لتبقي شاملة للمستقبل
    for i in range(1, 91):
        # حساب الانحرافات لمعادلة نبتون
        homo_dev = abs((i / homo_k) - round(i / homo_k))
        eris_dev = abs((i / eris_k) - round(i / eris_k))
        neptune_dev = abs((i / neptune_k) - round(i / neptune_k))
        
        # هل نبتون يعطي حالة حرجة؟
        neptune_critical = (homo_dev <= tolerance and eris_dev <= tolerance and neptune_dev <= tolerance)
        
        # حساب حالة زحل لهذه السنة العمرية بناءً على الدورات الكونية (كل دورة 4.4)
        saturn_status = "Normal"
        for cycle in range(1, 16):
            cycle_value = cycle * 4.4
            # إذا طابقت السنة العمرية الحالية بداية أو ذروة الدورة
            if int(cycle_value) == i:
                if cycle == 10:
                    saturn_status = "Apex Resonance"
                elif cycle == 9:
                    saturn_status = "Critical"
                break
        
        # السنة الميلادية المستهدفة
        target_year = birth_date.year + i
        
        # تطبيق منطق الفحص المشترك:
        # البحث يكون هل نبتون يعطي critical؟ في حال نعم نرى زحل، وإلا فهي سنة طبيعية
        if neptune_critical:
            if saturn_status in ["Apex Resonance", "Critical"]:
                # تحقق الشرطين: نكتب السنة فقط دون شهر أو يوم منعا للرعب
                results.append(f"Year: {target_year} | Job Or Social Status Transformation Expected")
      
    return results

def main(page: ft.Page):
    try:
        page.title = "Saturnian Neptune Eris Radar"
        page.padding = 20

        # ==================== 2. Security (Device ID & Key Checking) ====================
        def get_device_id():
            if os.path.exists(ID_FILE):
                with open(ID_FILE, "r") as f:
                    return f.read().strip()
            else:
                new_id = uuid.uuid4().hex[:8].upper()
                with open(ID_FILE, "w") as f:
                    f.write(new_id)
                return new_id

        def generate_password(mid):
            digits = ''.join(filter(str.isdigit, str(mid)))
            num = int(digits[:8]) if digits else int(str(mid).encode().hex(), 16)
            return str(round(abs(num / 2 * 3.14)))[:6]

        # ==================== 3. Main Application UI ====================
        def load_main_app():
            page.controls.clear()

            def on_generate(e):
                results_col.controls.clear()
                date_str = birth_input.value.strip()
                try:
                    b_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                    # تشغيل المحرك الحسابي المدمج بدون استخدام pandas
                    matrix_data = run_combined_matrix_engine(b_date)
                    
                    # بناء النص النهائي للعرض بشكل منظم وسطر بسطر
                    result_str = "="*50 + "\n"
                    result_str += f"📊 Matrix Inception: {b_date.strftime('%Y-%m-%d')}\n"
                    
                    result_str += "="*50 + "\n"
                    for row in matrix_data:
                        result_str += row + "\n"
                    result_str += "="*50 + "\n"
                    
                    results_col.controls.append(
                        ft.Text(result_str, font_family="monospace", size=12, selectable=True)
                    )
                except Exception as ex:
                    results_col.controls.append(ft.Text("Error: Please use format YYYY-MM-DD", size=14))
                page.update()

            birth_input = ft.TextField(label="Enter Birth Date YYYY-MM-DD", value="1981-04-17")
            results_col = ft.Column(spacing=5)
            
            scroll_box = ft.Container(
                content=ft.Column([results_col], scroll=ft.ScrollMode.AUTO),
                height=500,
                expand=True,
            )

            page.add(
                ft.Text("Saturnian Neptune Eris Radar", size=24, weight="bold"),
                birth_input,
                ft.ElevatedButton("Run Calculation", on_click=on_generate),
                scroll_box
            )
            page.update()

        # ==================== 4. Authentication Flow ====================
        # التحقق إذا كان ملف المفتاح موجوداً مسبقاً فلا يطلب التفعيل مرة أخرى أبداً
        if os.path.exists(KEY_FILE):
            load_main_app()
        else:
            mid = get_device_id()
            
            def on_activate(e):
                pwd = activation_input.value.strip()
                if pwd == generate_password(mid):
                    with open(KEY_FILE, "w") as f:
                        f.write(pwd)
                    load_main_app() 
                else:
                    error_msg.value = "Invalid Activation Key."
                    error_msg.visible = True
                    page.update()

            activation_input = ft.TextField(
                label="Enter Activation Key:", 
                password=True, 
                can_reveal_password=True
            )
            error_msg = ft.Text(value="", visible=False)

            page.add(
                ft.Text("Saturnian Neptune Eris Radar - Security Activation Required", size=20, weight="bold"),
                ft.Text("Send your Machine ID to programmer email : mulham81ahmed@gmail.com"),
                ft.Text(f"Machine ID: {mid}", size=16),
                activation_input,
                ft.ElevatedButton("Activate", on_click=on_activate),
                error_msg
            )
            page.update()

    except Exception as e:
        err_msg = traceback.format_exc()
        page.controls.clear()
        page.add(ft.Text("ERROR:", weight="bold"))
        page.add(ft.Text(err_msg, size=12))
        page.update()

ft.app(target=main)