# הוספת גיליון חדש
1. הוסף אובייקט ל-issues.json: slug, title, date (תאריך אמיתי), url, access ("full" או "partial"), summary_he {tldr, points[], audience, tags[], note}.
2. הסיכום נכתב מהתוכן המלא של הגיליון (ממשק ה-API הציבורי של blog.dailydoseofds.com), לא מהכותרת.
3. הרץ: python3 build.py
4. עשה commit ל-issues.json ול-index.html.
כללים: לא להעתיק הצעות מבצע או קודי הנחה מחלקי החסות. לסמן חסות ב-note. אם התוכן לא נגיש במלואו, access="partial".
