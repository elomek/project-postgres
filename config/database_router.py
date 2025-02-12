class ForcePostgresqlRouter:
    """
    این روتر تمام عملیات‌های جدید را به PostgreSQL می‌فرستد
    اما داده‌های قدیمی SQLite3 همچنان در دسترس باقی می‌مانند.
    """

    def db_for_read(self, model, **hints):
        """ خواندن داده‌های قدیمی از SQLite3، ولی خواندن بقیه از PostgreSQL """
        if hints.get('old_data'):  # اگر مشخص شود که داده قدیمی است، از SQLite3 بخواند
            return 'default'
        return 'postgresql'  # بقیه خواندن‌ها از PostgreSQL انجام شود

    def db_for_write(self, model, **hints):
        """ تمام نوشتن‌ها فقط در PostgreSQL انجام شود """
        return 'postgresql'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ همه مهاجرت‌ها فقط روی PostgreSQL انجام شود """
        return db == 'postgresql'
