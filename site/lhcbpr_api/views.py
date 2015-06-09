import sys
from lhcbpr_api.models import (Application, ApplicationVersion,
                               Option, Attribute, SetupProject,
                               JobDescription, AttributeGroup,
                               AttributeThreshold, Handler, JobHandler,
                               HandlerResult, AddedResult, Job,
                               JobResult, Platform, Host)

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins

from rest_framework.response import Response
from serializers import *
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import detail_route, list_route

import logging
logger = logging.getLogger(__name__)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationVersionViewSet(viewsets.ModelViewSet):
    queryset = ApplicationVersion.objects.all()
    serializer_class = ApplicationVersionSerializer


class OptionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class AttributeGroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AttributeGroup.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AttributeGroupListSerializer
        else:
            return AttributeGroupRetrieveSerializer

class AttributeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeThresholdViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AttributeThreshold.objects.all()
    serializer_class = AttributeThresholdSerializer


class SetupProjectViewSet(viewsets.ModelViewSet):
    queryset = SetupProject.objects.all()
    serializer_class = SetupProjectSerializer


class JobDescriptionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer


class HandlerViewSet(viewsets.ModelViewSet):
    queryset = Handler.objects.all()
    serializer_class = HandlerSerializer


class JobHandlerViewSet(viewsets.ModelViewSet):
    queryset = JobHandler.objects.all()
    serializer_class = JobHandlerSerializer


class HandlerResultViewSet(viewsets.ModelViewSet):
    queryset = HandlerResult.objects.all()
    serializer_class = HandlerResultSerializer


class JobResultViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = JobResult.objects.all()
    serializer_class = JobResultSerializer

class JobResultNoJobViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = JobResult.objects.all()
    serializer_class = JobResultNoJobSerializer


class JobResultByOptionAndAttribute(viewsets.ViewSet):
    queryset = JobResult.objects.all()

    def list(self, request, option, attr):
        queryset = JobResult.objects.filter(
            job__job_description__option__pk=option, attr__pk=attr)
        serializer = JobResultSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class JobViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class PlatformViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class HostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ActiveApplicationViewSet(viewsets.ViewSet):

    def list(self, request):
        id_field = 'job_description__application_version__application__id'
        name_field = 'job_description__application_version__application__name'
        queryset = (
            Job.objects
            .select_related()
            .values(id_field, name_field)
            .annotate(njobs=Count(id_field))
            .order_by(name_field)
        )
        result = []
        for app in queryset:
            result.append(
                {"id": app[id_field],
                 "name": app[name_field],
                 "count": app["njobs"]
                 }
            )
        return Response(result)

    def retrieve(self, request, pk=None):
        queryset = Application.objects.all()
        app = get_object_or_404(queryset, pk=pk)
        serializer = ApplicationSerializer(app, context={'request': request})
        return Response(serializer.data)

    @list_route()
    def versions(self, request, pk):
        id_field = 'job_description__application_version__id'
        name_field = 'job_description__application_version__version'
        time_field = 'job_description__application_version__vtime'
        slot_id_field = 'job_description__application_version__slot__id'
        slot_field = 'job_description__application_version__slot__name'
        
        result = []
        # Releases
        queryset = (
            Job.objects
            .select_related()
            .values(id_field, name_field, time_field)
            .filter(
                job_description__application_version__slot__isnull=True,
                job_description__application_version__application__id=pk)
            .annotate(njobs=Count(id_field))
            .order_by('-'+time_field)
        )
        releases = []
        for app in queryset:
            releases.append(
                {"id": app[id_field],
                 "name": app[name_field],
                 "count": app["njobs"]
                }
            )
        result.append({'name': 'Releases', 'values': releases})
        
        # Slots
        queryset = (
            Job.objects
            .select_related()
            .values(slot_id_field, slot_field)
            .filter(
                job_description__application_version__slot__isnull=False,
                job_description__application_version__application__id=pk)
            .annotate(njobs=Count(slot_id_field))
            .order_by(slot_field)
        )

        slots = []
        for slot in queryset:
            slot_record = {'name': slot[slot_field]}
            queryset_per_slot = (
                Job.objects
                .select_related()
                .values(id_field, name_field, time_field)
                .filter(
                    job_description__application_version__slot__id=slot[slot_id_field],
                    job_description__application_version__application__id=pk
                )
                .annotate(njobs=Count(id_field))
                .order_by('-' + time_field)[:7]
            )
            slot_values = []
            for app in queryset_per_slot:
                slot_values.append(
                    {   
                        "id": app[id_field],
                        "name": app[name_field],
                        "count": app["njobs"]
                    }
                )
            slot_record["values"] = slot_values
            slot_record["count"] = slot["njobs"]
            if slot_values:
                result.append(slot_record)   
        
        return Response(result)

    @list_route()
    def slots(self, request, pk):
        id_field = 'job_description__application_version__slot__id'
        name_field = 'job_description__application_version__slot__name'
        queryset = (
            Job.objects
            .select_related()
            .values(id_field, name_field)
            .filter(job_description__application_version__slot__id__isnull=False, job_description__application_version__application__id=pk)
            .annotate(njobs=Count(id_field))
        )
        result = []
        for app in queryset:
            result.append(
                {"id": app[id_field],
                 "name": app[name_field],
                 "count": app["njobs"]
                 }
            )
        return Response(result)

    @list_route()
    def options(self, request, pk):
        id_field = 'job_description__option__id'
        name_field = 'job_description__option__content'

        versions = []
        if 'versions' in request.query_params and request.query_params['versions']:
            versions = [
                int(v) for v in request.query_params['versions'].split(',')
            ]

        queryset = (Job.objects.select_related().values(id_field, name_field)
                    .filter(
                        job_description__application_version__application__id=pk
        ))
        if versions:
            queryset = queryset.filter(
                job_description__application_version__id__in=versions)
        queryset = queryset.annotate(njobs=Count(id_field))

        result = []
        for option in queryset:
            result.append(
                {"id": option[id_field],
                 "name": option[name_field],
                 "count": option["njobs"]
                 }
            )

        return Response(result)


class SearchJobsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        id_field = 'job_description__application_version__application__id'
        name_field = 'job_description__application_version__application__name'
        queryset = (
            Job.objects
            .select_related()
            .order_by("-id")
        )
        application = self.request.query_params.get("application", None)
        if application:
            ids = application.split(',')
            queryset = queryset.filter(
                job_description__application_version__application__id__in=ids)

        versions = self.request.query_params.get("versions", None)
        if versions:
            ids = versions.split(',')
            queryset = queryset.filter(
                job_description__application_version__id__in=ids)

        options = self.request.query_params.get("options", None)
        if options:
            ids = options.split(',')
            queryset = queryset.filter(job_description__option__id__in=ids)
        
        return queryset.order_by('-time_end')
        # serializer = JobListSerializer(queryset, many=True, read_only=True, context={'request': request})
        # return Response(serializer.data)



    def retrieve(self, request, pk=None):
        queryset = Job.objects.all()
        job = get_object_or_404(queryset, pk=pk)
        serializer = JobSerializer(job, context={'request': request})
        return Response(serializer.data)

    @list_route()
    def versions(self, request, pk):
        id_field = 'job_description__application_version__id'
        name_field = 'job_description__application_version__version'
        queryset = (
            Job.objects
            .select_related()
            .values(id_field, name_field)
            .filter(job_description__application_version__application__id=pk)
            .annotate(njobs=Count(id_field))
        )
        result = []
        for app in queryset:
            result.append(
                {"id": app[id_field],
                 "name": app[name_field],
                 "count": app["njobs"]
                 }
            )
        serializer = ActiveItemSerializer(result,many=True, read_only=True)
        return Response(serializer.data)

    @list_route()
    def options(self, request, pk):
        id_field = 'job_description__option__id'
        name_field = 'job_description__option__content'

        versions = []
        if 'versions' in request.query_params and request.query_params['versions']:
            versions = [
                int(v) for v in request.query_params['versions'].split(',')
            ]

        queryset = (Job.objects.select_related().values(id_field, name_field)
                    .filter(job_description__application_version__application__id=pk))
        if versions:
            queryset = queryset.filter(
                job_description__application_version__id__in=versions)
        queryset = queryset.annotate(njobs=Count(id_field))

        result = []
        for option in queryset:
            result.append(
                {"id": option[id_field],
                 "name": option[name_field],
                 "count": option["njobs"]
                 }
            )

        serializer = ActiveItemSerializer(result, many=True, read_only=True)
        return Response(serializer.data)

class CompareJobsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = AttributesWithJobResultsSerializer
    
    def get_queryset(self):
        context = self.get_serializer_context()
        results = Attribute.objects
        if context["attrs"]:
            results = results.filter(id__in=context["attrs"])
        if context["contains"]:
            results = results.filter(name__icontains=context["contains"])
        results = results.filter(jobresults__job__id__in=context["ids"])
        return results.order_by('name').distinct()

    def get_serializer_context(self):
        result = {"ids": [], "attrs": [], "request": self.request, "contains": None}
        if 'ids' in self.request.query_params:
            result["ids"] = [int(id) for id in self.request.query_params['ids'].split(',')]
        if 'attrs' in self.request.query_params:
            result["attrs"] = [int(id) for id in self.request.query_params['attrs'].split(',')]        
        
        if 'contains' in self.request.query_params:
            result['contains'] = self.request.query_params['contains']

        return result

class TrendsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TrendsSerializer
    
    def get_queryset(self):
        context = self.get_serializer_context()
        queryset = JobResult.objects
        if context['app']:
            queryset = queryset.filter(job__job_description__application_version__application__id__in = context['app'])
        if context['options']:
            queryset = queryset.filter(job_description__option__id__in = context['options'])
        queryset = queryset.select_related(
            'attr__name', 
            'job__job_description__application_version__version'
        )
        queryset = queryset.filter(attr__dtype__in = ['Float', 'Integer'])
        queryset = queryset.order_by('attr__id')
        queryset = queryset.values(
            'attr__id', 
            'attr__name',
            'job__job_description__application_version__version',
            'resultinteger',
            'resultfloat'
        )

        results = []
        current_attr_id = None
        current_result_index = -1
        current_version = None
        current_version_index = -1
        for item in queryset:
            if current_version_index > -1 and (item['attr__id'] != current_attr_id or item['job__job_description__application_version__version'] != current_version):
                numbers = results[current_result_index]['values'][current_version_index]['results']
                count = float(len(numbers))
                average = sum(numbers) / count
                deviation = 0
                for n in numbers:
                    deviation = deviation + abs(average - n)
                deviation = deviation / count
                results[current_result_index]['values'][current_version_index] = {
                    'version': current_version,
                    'average': average,
                    'deviation': deviation
                }
            if item['attr__id'] != current_attr_id:
                results.append({
                    'id': item['attr__id'],
                    'name': item['attr__name'],
                    'values': []
                })
                current_result_index = current_result_index + 1
                current_attr_id = item['attr__id']
                current_version = None
                current_version_index = -1
            if item['job__job_description__application_version__version'] != current_version:
                current_version = item['job__job_description__application_version__version']
                results[current_result_index]['values'].append({
                    'version': current_version,
                    'results': []
                })
                current_version_index = current_version_index + 1
            if item['resultfloat']:
                results[current_result_index]['values'][current_version_index]['results'].append(item['resultfloat'])
            else:
                results[current_result_index]['values'][current_version_index]['results'].append(item['resultinteger'])

        if current_version_index > -1:
            numbers = results[current_result_index]['values'][current_version_index]['results']
            count = float(len(numbers))
            average = sum(numbers) / count
            deviation = 0
            for n in numbers:
                deviation = deviation + abs(average - n)
            deviation = deviation / count
            results[current_result_index]['values'][current_version_index] = {
                'version': current_version,
                'average': average,
                'deviation': deviation
            }

        return results

    def get_serializer_context(self):
        result = {"app": None, "options": None, "request": self.request}
        if 'app' in self.request.query_params:
            result["app"] = [int(id) for id in self.request.query_params['app'].split(',')]
        if 'options' in self.request.query_params:
            result["options"] = [int(id) for id in self.request.query_params['options'].split(',')]
        return result
