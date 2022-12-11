from django.contrib import admin
from .models import Tests, Quiz, Question, Answer, Marks_Of_User, QuesModel


admin.site.register(Tests)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Marks_Of_User)
admin.site.register(QuesModel)

