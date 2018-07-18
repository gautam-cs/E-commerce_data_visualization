from django.conf.urls import include, url
from . import view

urlpatterns = [
    url(r'^$', view.home, name='home'),
	url(r'^error_page$', view.error_page, name='error_page'),
	url(r'^sample$', view.sample, name='sample_queries'),

	################################ Graph visualisation #################################
	url(r'^graph_bar_2$', view.graph_bar_2, name='graph_bar_2'),
	url(r'^graph_bar_3$', view.graph_bar_3, name='graph_bar_3'),
	url(r'^dicision_tree$', view.dicision_tree, name='dicision_tree'),
	url(r'^trend_2$', view.trend_2, name='trend_2'),
	url(r'^trend_3$', view.trend_3, name='trend_3'),
	url(r'^segment$', view.segment, name='segment'),
	]
