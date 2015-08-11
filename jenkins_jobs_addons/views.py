"""
Views show TODO

**Component**: views
  :Macro: views
  :Entry Point: jenkins_jobs.views
"""


import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base


def all_view(parser, xml_parent, data):
    """yaml: all_view
    All view
    :arg bool filter-executors: only those build executors will be shown that
                                could execute the jobs in this view.
    :arg bool filter-queue: only jobs in this view will be shown in the queue.

    Example:

    .. literalinclude::  /../../tests/views/fixtures/all_view.yaml
    """
    view = XML.SubElement(xml_parent, 'hudson.model.AllView')
    XML.SubElement(view, 'name').text = 'All'

    executors = data.get('filter-executors', False)
    XML.SubElement(view, 'filterExecutors').text = str(executors).lower()

    queue = data.get('filter-queue', False)
    XML.SubElement(view, 'filterQueue').text = str(queue).lower()

    properties_attributes = dict()
    properties_attributes['class'] = 'hudson.model.View$PropertyList'
    XML.SubElement(view, 'properties', attrib=properties_attributes)


def delivery_pipeline_view(parser, xml_parent, data):

    delivery_pipeline = 'se.diabol.jenkins.pipeline.DeliveryPipelineView'

    view = XML.SubElement(xml_parent, delivery_pipeline)
    in_folder = data.get('folder', False)
    if in_folder:
        owner_attrs = dict()
        owner_attrs['class'] = 'com.cloudbees.hudson.plugins.folder.Folder'
        owner_attrs['reference'] = '../../..'
    XML.SubElement(view, 'owner', attrib=owner_attrs)

    XML.SubElement(view, 'name').text = data.get('name')

    executors = data.get('filter-executors', False)
    XML.SubElement(view, 'filterExecutors').text = str(executors).lower()

    queue = data.get('filter-queue', False)
    XML.SubElement(view, 'filterQueue').text = str(queue).lower()

    properties_attributes = dict()
    properties_attributes['class'] = 'hudson.model.View$PropertyList'
    XML.SubElement(view, 'properties', attrib=properties_attributes)

    xml_components = XML.SubElement(view, 'componentSpecs')
    components = data.get('components', [])
    for component in components:
        print component
        spec_class = "se.diabol.jenkins.pipeline."\
                     "DeliveryPipelineView_-ComponentSpec"
        component_spec = XML.SubElement(xml_components, spec_class)
        name = component.get('name')
        XML.SubElement(component_spec, 'name').text = name
        first_job = component.get('first-job')
        XML.SubElement(component_spec, 'firstJob').text = first_job

    number_of_pipelines = str(data.get('number-of-pipelines', 3))
    XML.SubElement(
        view, 'noOfPipelines').text = number_of_pipelines

    aggregated_pipeline_raw = data.get('show-aggregated-pipeline', False)
    aggregated_pipeline = str(aggregated_pipeline_raw).lower()
    XML.SubElement(view, 'showAggregatedPipeline').text = aggregated_pipeline

    number_of_columns = str(data.get('number-of-columns', 1))
    XML.SubElement(view, 'noOfColumns').text = number_of_columns

    sorting_options = ['none', 'Name', 'LatestActivity']
    sorting = data.get('sorting', 'none')

    if sorting not in sorting_options:
        raise ValueError('sorting must be one of {} '.format(sorting_options))

    if sorting == 'none':
        XML.SubElement(view, 'sorting').text = 'none'
    else:
        XML.SubElement(
            view, 'sorting'
        ).text = 'se.diabol.jenkins.pipeline.sort.{}Comparator'.format(sorting)

    show_avatars = data.get('show-avatars', False)
    XML.SubElement(view, 'showAvatars').text = str(show_avatars).lower()

    update_interval = str(data.get('update-interval', 1))
    XML.SubElement(view, 'updateInterval').text = update_interval

    show_changes = str(data.get('show-changes', False)).lower()
    XML.SubElement(view, 'showChanges').text = str(show_changes).lower()

    manual_triggers = str(data.get('allow-manual-triggers', False)).lower()
    XML.SubElement(view, 'allowManualTriggers').text = manual_triggers

    total_build_time = str(data.get('show_total_build_time', False)).lower()
    XML.SubElement(view, 'showTotalBuildTime').text = total_build_time

    allow_rebuild = str(data.get('allow-rebuild', False)).lower()
    XML.SubElement(view, 'allowRebuild').text = allow_rebuild

    pipeline_start = str(data.get('allow-pipeline-start', False)).lower()
    XML.SubElement(view, 'allowPipelineStart').text = pipeline_start

    show_description = str(data.get('show-description', False)).lower()
    XML.SubElement(view, 'showDescription').text = show_description

    show_promotions = str(data.get('show-promotions', False)).lower()
    XML.SubElement(view, 'showPromotions').text = show_promotions

    xml_jobs = XML.SubElement(view, 'regexpFirstJobs')
    jobs = data.get('regexp-first-jobs', [])
    for job in jobs:
        xml_job = XML.SubElement(xml_jobs, 'se.diabol.jenkins.pipeline.'
                                           'DeliveryPipelineView_-RegExpSpec')
        XML.SubElement(xml_job, 'regexp').text = job


def build_pipeline_view(parser, xml_parent, data):
    """ Creates a view properties """
    build_pipeline = 'au.com.centrumsystems.hudson.plugin.'\
                     'buildpipeline.BuildPipelineView'

    view = XML.SubElement(xml_parent, build_pipeline)

    in_folder = data.get('folder', False)
    if in_folder:
        owner_attrs = dict()
        owner_attrs['class'] = 'com.cloudbees.hudson.plugins.folder.Folder'
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    XML.SubElement(view, 'name').text = data.get('name')

    executors = data.get('filter-executors', False)
    XML.SubElement(view, 'filterExecutors').text = str(executors).lower()

    queue = data.get('filter-queue', False)
    XML.SubElement(view, 'filterQueue').text = str(queue).lower()

    properties_attributes = dict()
    properties_attributes['class'] = 'hudson.model.View$PropertyList'
    XML.SubElement(view, 'properties', attrib=properties_attributes)

    grid_attrs = dict()
    grid_attrs['class'] = 'au.com.centrumsystems.hudson.plugin.buildpipeline.'\
                          'DownstreamProjectGridBuilder'
    grid = XML.SubElement(view, 'gridBuilder', attrib=grid_attrs)
    first_job = data.get('first-job', None)
    XML.SubElement(grid, 'firstJob').text = first_job

    display_number_of_builds = str(data.get('display-number-of-builds', 10))
    XML.SubElement(view, 'noOfDisplayedBuilds').text = display_number_of_builds

    build_view_title = data.get('build-view-title')
    XML.SubElement(view, 'buildViewTitle').text = build_view_title

    console_output_links = ['This Window', 'New Window', 'Light Box']
    console_output_link_style = data.get(
        'console_output_link-style', 'Light Box')

    if console_output_link_style not in console_output_links:
        raise ValueError('console_output_link-style must '
                         'be one of {}'.format(console_output_links))

    XML.SubElement(
        view, 'consoleOutputLinkStyle'
    ).text = console_output_link_style

    XML.SubElement(view, 'cssUrl').text = data.get('cssUrl')

    job = XML.SubElement(view, 'triggerOnlyLatestJob')
    job.text = str(data.get('trigger-only-latest-job', False)).lower()

    manual_trigger = data.get('always-allow-manual-trigger', False)
    manual_trigger = str(manual_trigger).lower()
    XML.SubElement(
        view, 'alwaysAllowManualTrigger'
    ).text = manual_trigger

    parmas = str(data.get('show-pipeline-parameters', False)).lower()
    XML.SubElement(view, 'showPipelineParameters').text = parmas

    headers_raw = data.get('show-pipeline-parameters-in-header', False)
    headers = str(headers_raw).lower()
    XML.SubElement(
        view, 'showPipelineParametersInHeaders'
    ).text = headers

    start_with_params = str(data.get('start-with-params', False)).lower()
    XML.SubElement(
        view, 'startsWithParameters'
    ).text = start_with_params

    refresh_freq = data.get('refresh-frequency', 3)
    XML.SubElement(view, 'refreshFrequency').text = str(refresh_freq)

    show_def_raw = data.get('show-pipeline-definition-in-headers', False)
    show_def = str(show_def_raw).lower()
    XML.SubElement(view, 'showPipelineDefinitionHeader').text = show_def


class Views(jenkins_jobs.modules.base.Base):
    sequence = 20

    component_type = 'view'
    component_list_type = 'views'

    def gen_xml(self, parser, xml_parent, data):
        views = XML.SubElement(xml_parent, 'views')

        for view in data.get('views', []):
            self.registry.dispatch('view', parser, views, view)
