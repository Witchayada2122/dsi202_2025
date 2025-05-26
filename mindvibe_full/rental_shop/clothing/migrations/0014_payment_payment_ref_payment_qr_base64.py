from django.db import migrations, models
import uuid

def generate_uuids(apps, schema_editor):
    Payment = apps.get_model('clothing', 'Payment')
    for payment in Payment.objects.all():
        if not payment.payment_ref:
            payment.payment_ref = uuid.uuid4()
            payment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0013_payment_return_item_code_payment_return_proof_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_ref',
            field=models.UUIDField(default=uuid.uuid4, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='qr_base64',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(generate_uuids),  
    ]
