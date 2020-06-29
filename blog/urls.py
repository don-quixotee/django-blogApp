from django.urls import path
from blog.views import PostListView,  PostDetailView, contact_us_form_view,  PostCreateView, PostUpdateView, PostDeleteView, profileDetailView, SearchListView, BookmarkView, CommentDeleteView, bookmarkDeleteView




urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    # path('blog', blogList),
    path('blogs/<slug:slug>', PostDetailView.as_view(), name='post-detail'),
    path('contactUs/', contact_us_form_view, name='contactUs'),
    path('category/<int:id>/', PostListView.as_view(), name='post_by_category'),

    path('post/',PostCreateView.as_view() , name='post'),
    path('update/<slug:slug>/', PostUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/', profileDetailView.as_view(), name='profile'),
    path('search/', SearchListView, name='search'),
    path('blog/bookmark', BookmarkView.as_view(),name='bookmark'),
    path('blog/<int:pk>/add_bookmark', BookmarkView.as_view(), name='add-bookmark' ),
    path('comment/<int:id>/',CommentDeleteView, name='commentDelete' ),
    path('bookmark/<int:id>/', bookmarkDeleteView, name='bookmarkDelete')


]