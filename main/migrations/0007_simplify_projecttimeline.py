# Generated manually to simplify ProjectTimeline model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_projecttimeline'),
    ]

    operations = [
        # Remove fields we don't need
        migrations.RemoveField(
            model_name='projecttimeline',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='projecttimeline',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='projecttimeline',
            name='progress_percentage',
        ),
        migrations.RemoveField(
            model_name='projecttimeline',
            name='is_completed',
        ),
        # Update status choices for simpler workflow steps
        migrations.AlterField(
            model_name='projecttimeline',
            name='status',
            field=models.CharField(
                choices=[
                    ('consultation', 'Tư Vấn & Thiết Kế'),
                    ('planning', 'Lập Kế Hoạch & Vật Liệu'),
                    ('production', 'Sản Xuất & Chế Tác'),
                    ('installation', 'Thi Công & Lắp Đặt'),
                    ('completion', 'Nghiệm Thu & Bàn Giao'),
                ],
                max_length=20
            ),
        ),
    ]
