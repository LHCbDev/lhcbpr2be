from django.core.management.base import BaseCommand
import lhcbpr.models as v1
import lhcbpr_api.models
from lhcbpr_api.models import *

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Synchronize with v1 database"


    def handle(self, *args, **options):
        # Applications

        for app_source in v1.Application.objects.using('v1').all():
            self._application(app_source)
 
        # Options
        for option_source in v1.Options.objects.using('v1').all():
            self._option(option_source)
  
        # Setup project
        for setup_source in v1.SetupProject.objects.using('v1').all():
            self._setup_project(setup_source)

        # Job descriptions
        for jd_source in v1.JobDescription.objects.using('v1').all():
            self._job_description(jd_source)
            

        # Platform
        for pl_source in v1.Platform.objects.using('v1').all():
            self._platform(pl_source)

        # Handler
        for handler_source in v1.Handler.objects.using('v1').all():
            self._handler(handler_source)

        # JobHandler
        for jh_source in v1.JobHandler.objects.using('v1').all():
            self._job_handler(jh_source)


        # Host
        for host_source in v1.Host.objects.using('v1').all():
            self._host(host_source)

        # Job
        njobs = v1.Job.objects.using('v1').count()
        logger.info("Number of jobs in V1 %d" % njobs)
        for job_source in v1.Job.objects.using('v1').order_by('-time_start'):
            self._job(job_source)
            njobs -= 1
            logger.info("Jobs to process: %d" % njobs) 
   

        # Attribute groups
        # for ja_source in v1.JobAttribute.objects.using('v1').all():
        #     self._job_attribute(ja_source)

        # Attribute groups
        # for group_source in v1.JobAttribute.objects.using('v1').values_list('group', flat=True).distinct():
        #     self._group(group_source)


    def _application(self, app_source):
        app_target = Application.objects.filter(name=app_source.appName)
        if not app_target:
            app_target = Application.objects.create(    name=app_source.appName)
            app_target.save()
        else:
            app_target = app_target[0]

        app_version_target = ApplicationVersion.objects.filter(
            version=app_source.appVersion, application=app_target)
        
        if not app_version_target:
            is_nightly = ApplicationVersion.is_it_nightly(app_source.appVersion)
            
            slot = None 
            slotname = None
            number = None
            vtime = None
            
            if is_nightly:
                res = ApplicationVersion.get_slot_and_number(app_source.appVersion)

                if res:
                    slotname,number,vtime = res
                else:
                    slotname = app_source.appVersion
                if slotname:    
                    slots = Slot.objects.filter(name=slotname)
                    if not slots:
                        slot = Slot.objects.create(name=slotname)
                    else:
                        slot = slots[0]

            app_version_target = ApplicationVersion.objects.create(
                version=app_source.appVersion,
                application=app_target,
                slot=slot,
                vtime=vtime,
                is_nightly=is_nightly
            )
            app_version_target.save()
        else:
            app_version_target = app_version_target[0]

        return app_version_target

    def _option(self, option_source):
        option_target = Option.objects.filter(
            old_id=option_source.id
        )
        if not option_target:
            option_target = Option.objects.create(
                content=option_source.content,
                description=option_source.description,
                old_id=option_source.id
            )
            option_target.save()
        else:
           option_target = option_target[0] 
        return option_target

    def _setup_project(self, setup_source):
        setup_target = SetupProject.objects.filter(
            old_id=setup_source.id
        )
        if not setup_target:
            setup_target = SetupProject.objects.create(
                content=setup_source.content,
                description=setup_source.description,
                old_id=setup_source.id
            )
            setup_target.save()
        else:
            setup_target = setup_target[0]
        return setup_target

    def _job_description(self, jd_source):
        jd_target = JobDescription.objects.filter(old_id=jd_source.id)
        if not jd_target:
            ver = self._application(jd_source.application)
            opt = self._option(jd_source.options)
            if jd_source.setup_project:
                setup = SetupProject.objects.filter(old_id=jd_source.setup_project.id)[0]
            else:
                setup = None
            jd_target = JobDescription.objects.create(application_version=ver, option=opt, setup_project=setup, old_id=jd_source.id)
            jd_target.save()
        else:
            jd_target = jd_target[0]
        return jd_target

    def _platform(self, pl_source):
        if not pl_source:
            return None

        pl_target = Platform.objects.filter(old_id=pl_source.id)
        if not pl_target:
            pl_target = Platform.objects.create(
                cmtconfig=pl_source.cmtconfig,
                old_id=pl_source.id)
            pl_target.save()
        else:
            pl_target = pl_target[0]

        return pl_target

    def _handler(self, handler_source):
        handler_target = Handler.objects.filter(old_id=handler_source.id)
        if not handler_target:
            handler_target = Handler.objects.create(
                name=handler_source.name,
                description=handler_source.description,
                old_id=handler_source.id
            )
            handler_target.save()
        else:
            handler_target = handler_target[0]
        return handler_target

    def _job_handler(self, jh_source):
 
        jh_target = JobHandler.objects.filter(old_id=jh_source.id)
        if not jh_target:
            jd = self._job_description(jh_source.jobDescription)
            handler = self._handler(jh_source.handler)

            jh_target = JobHandler.objects.create(
                job_description=jd,
                handler=handler,
                old_id=jh_source.id
            )
            jh_target.save()
        else:
            jh_target = jh_target[0]
        return jh_target

    def _host(self, host_source):
        if not host_source:
            return None

        host_target = Host.objects.filter(old_id=host_source.id)
        if not host_target:
            host_target = Host.objects.create(
                hostname=host_source.hostname,
                cpu_info=host_source.cpu_info,
                memory_info=host_source.memoryinfo,
                old_id=host_source.id
            )
            host_target.save()
        else:
            host_target = host_target[0]
        return host_target

    def _job(self, job_source):
        job_target = Job.objects.filter(old_id=job_source.id)
        if not job_target:
            host = self._host(job_source.host)
            job_description = self._job_description(job_source.jobDescription)
            platform = self._platform(job_source.platform)

            job_target = Job.objects.create(
                host=host,
                job_description=job_description,
                platform=platform,
                time_start=job_source.time_start,
                time_end=job_source.time_end,
                status=job_source.status,
                is_success=job_source.success,
                old_id=job_source.id)
            job_target.save()
            for jr_source in job_source.jobresults.all():
                self._job_result(jr_source, job_target)

        else:
            job_target = job_target[0]
        return job_target

    def _group(self, group_source):
        if not group_source:
            return None

        group_target = AttributeGroup.objects.filter(name=group_source)
        if not group_target:
            group_target = AttributeGroup.objects.create(
                name=group_source
            )
            group_target.save()
        else:
            group_target = group_target[0]
        return group_target

    def _job_attribute(self, ja_source):
        if not ja_source:
            return None

        ja_target = Attribute.objects.filter(old_id=ja_source.id)
        if not ja_target:
            group = self._group(ja_source.group)
            ja_target = Attribute.objects.create(
                name=ja_source.name,
                dtype=ja_source.type,
                description=ja_source.description,
                old_id=ja_source.id)
            if group:
                ja_target.groups.add(group)
            ja_target.save()
        else:
            ja_target = ja_target[0]
        return ja_target

    def _job_result(self, jr_source, job):
        if not jr_source:
            return None

        attr = self._job_attribute(jr_source.jobAttribute)

        if attr.dtype == "String":
            source = v1.ResultString
        if attr.dtype == "Float":
            source = v1.ResultFloat
        if attr.dtype == "File":
            source = v1.ResultFile
        if attr.dtype == "Integer":
            source = v1.ResultInt
        target_class = getattr(lhcbpr_api.models, "Result"+attr.dtype)
        jr_target = target_class(job=job, attr=attr)
        
        attr_source = source.objects.using('v1').filter(job=jr_source.job, jobAttribute=jr_source.jobAttribute)
        if attr_source:
            attr_source = attr_source[0]
            jr_target.data = attr_source.file if attr.dtype == "File" else attr_source.data
            jr_target.save()
        else:
            logger.error(jr_source)
