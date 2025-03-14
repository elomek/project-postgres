'''class DefaultToPostgresRouter:
    def db_for_read(self, model, **hints):
        """همه عملیات‌های خواندن را روی PostgreSQL انجام بده"""
        return 'postgresql'

    def db_for_write(self, model, **hints):
        """همه عملیات‌های نوشتن را روی PostgreSQL انجام بده"""
        return 'postgresql'
    def db_for_delete(self, model, **hints):
        """همه عملیات‌های حذف را روی PostgreSQL انجام بده"""
        return 'postgresql'

    def db_for_update(self, model, **hints):
        """همه عملیات‌های به‌روزرسانی را روی PostgreSQL انجام بده"""
        return 'postgresql'

    def allow_relation(self, obj1, obj2, **hints):
        """اجازه‌ی ارتباط بین مدل‌های مختلف را بده"""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """همه migrations ها را روی PostgreSQL انجام بده"""
        return db == 'postgresql'''
