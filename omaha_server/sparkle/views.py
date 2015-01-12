# coding: utf8

"""
This software is licensed under the Apache 2 license, quoted below.

Copyright 2014 Crystalnix Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

import logging

from django.views.generic import ListView
from models import SparkleVersion


logger = logging.getLogger(__name__)



class SparkleView(ListView):
    http_method_names = ['get']
    queryset = SparkleVersion.objects.all()
    template_name = 'sparkle/appcast.xml'

    def get_queryset(self):
        qs = super(SparkleView, self).get_queryset()
        return qs.filter(channel__name=self.kwargs.get('channel'),
                         app__name=self.kwargs.get('app_name'))

    def get_context_data(self, **kwargs):
        context = super(SparkleView, self).get_context_data(**kwargs)
        context['app_name'] = self.kwargs.get('app_name')
        context['channel'] = self.kwargs.get('channel')
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(SparkleView, self).render_to_response(context, **response_kwargs)
        response['Content-Type'] = 'text/xml; charset=utf-8'
        return response
