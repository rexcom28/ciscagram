from django.urls import path, re_path
from django.urls.conf import include
from .views import (
    post_list_and_create,
    load_post_data_view,
    like_unlike_post,
    post_detail,
    post_detail_data_view,
    delete_post,
    update_post,
    image_upload_view,

    MainView,
    file_upload_view,
    search_results,
    categories,
    category_Add,
    category,
    categoryEdit
    

)
from .api import (api_categoryAddPost)

app_name = 'posts'

urlpatterns = [
    path('', post_list_and_create, name='main-board'),
    
    path('m/upload/', file_upload_view, name='upload-view'),
    path('search/', search_results, name='search'),
    
    

    path('like-unlike/', like_unlike_post, name='like-unlike'),
    path('upload/', image_upload_view, name='image-upload'),
    path('<int:pk>/upload/', image_upload_view, name='image-upload'),
    
    path('<int:pk>/', post_detail, name='post-detail'),
    path('<int:pk>/update/', update_post, name='post-update'),
    path('<int:pk>/delete/', delete_post, name='post-delete'),

    path('data/<int:num_posts>/', load_post_data_view, name='posts-data'),
    
    path('<int:pk>/data/', post_detail_data_view, name='post-detail-data'),
    path('categories/', categories, name='categories'),
    path('category/<str:category>/', category, name='category'),
    path('category_Add/', category_Add, name='categoryAdd'),
    path('category/<str:category>/edit/', categoryEdit, name='categoryEdit'),

    path('api_categoryAddPost/', api_categoryAddPost, name='category_add_post'),
]