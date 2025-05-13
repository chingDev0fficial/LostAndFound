from .models import Admin

def authenticate(username, password):
    admin_acc = Admin.objects.filter(username=username).first()
    print(admin_acc.check_password(password))
    if admin_acc and admin_acc.check_password(password):
        return True
    return False