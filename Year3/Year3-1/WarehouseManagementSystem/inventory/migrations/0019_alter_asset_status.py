from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0018_alter_item_is_serialized"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="status",
            field=models.CharField(
                choices=[
                    ("AVAILABLE", "可用"),
                    ("BORROWED", "借出"),
                    ("DAMAGED", "损坏"),
                    ("LOST", "丢失"),
                    ("OUT", "已出库"),
                ],
                default="AVAILABLE",
                max_length=20,
            ),
        ),
    ]
