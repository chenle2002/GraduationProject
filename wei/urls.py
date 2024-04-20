from django.urls import path

from .views import load_target_data, get_topic_syntax, get_ipc_from_text, load_other_data, build_syntax_by_target

urlpatterns = [
    path('getTopicSyntax/', get_topic_syntax, name='getTopicSyntax'),
    path('getIpc/', get_ipc_from_text, name='getIpc'),
    path('loadTargetData/', load_target_data, name='loadTargetData'),
    path('loadOtherData/', load_other_data, name='loadOtherData'),
    path('buildSyntaxByTarget/', build_syntax_by_target, name='buildSyntaxByTarget'),
]
