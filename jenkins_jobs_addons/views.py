"""
Views show job status.

**Component**: views
  :Macro: views
  :Entry Point: jenkins_jobs.views
"""


import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base


def all_view(parser, xml_parent, data):
    """
    All view

    :arg bool filter-executors: only those build executors will be shown that
      could execute the jobs in this view.
    :arg bool filter-queue: only jobs in this view will be shown in the queue.
    :arg bool folder: Wether or not this view is in a folder.


    Example:

    .. literalinclude::  /../tests/views/fixtures/all_view.yaml

    """
    view = XML.SubElement(xml_parent, 'hudson.model.AllView')
    XML.SubElement(view, 'name').text = 'All'
    in_folder = data.get('folder', False)
    owner_attrs = dict()
    if in_folder:
        owner_attrs['class'] = 'com.cloudbees.hudson.plugins.folder.Folder'
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    executors = data.get('filter-executors', False)
    XML.SubElement(view, 'filterExecutors').text = str(executors).lower()

    queue = data.get('filter-queue', False)
    XML.SubElement(view, 'filterQueue').text = str(queue).lower()

    properties_attributes = dict()
    properties_attributes['class'] = 'hudson.model.View$PropertyList'
    XML.SubElement(view, 'properties', attrib=properties_attributes)


def delivery_pipeline_view(parser, xml_parent, data):
    """
    Delivery Pipeline View requires the Jenkins `Delivery Pipeline Plugin.
    <https://wiki.jenkins-ci.org/display/JENKINS/Delivery+Pipeline+Plugin>`_

    :arg bool filter-executors: only those build executors will be shown that
      could execute the jobs in this view.
    :arg bool filter-queue: only jobs in this view will be shown in the queue.
    :arg bool folder: Wether or not this view is in a folder.
    :arg str name: The name of this view.
    :arg dict components: The components (jobs) for this pipeline:

        * **name** (str): Name of the pipeline, usually the name of the
                          component or product.
        * **first-job** (str): First job in the pipeline. Usually the
                             build/compile job. The build number/build
                             display name will be used as the version in
                             later tasks or stages. If using folders, it
                             should be a full path to the job.

    :arg int number-of-pipelines: Number of pipelines instances shown for each
                                  pipeline.
    :arg bool show-aggregated-pipeline: Show an aggregated view where each
                                        stage shows the latest version being
                                        executed.

    :arg int number-of-columns: Number of columns used for showing pipelines.
                                Useful for multiple components in the view to
                                show them beside each others.

    :arg int sorting: How to sort the pipeline in the view.
                      Only applicable for several pipelines.
                      Can be sorted by latest activity or by name.
    :arg int update-interval: How often will the view be updated in seconds.

    :arg bool allow-pipeline-start: Start a new pipeline build.

    :arg bool allow-manual-triggers: If a task is manual (Build other projects
      (manual step) from Build Pipeline Plugin, show a button.

    :arg bool allow-rebuild: Rebuild a task.

    :arg str show-avatars: Show avatars pictures instead of names of the people
      involved in a pipeline instance. Use the `Avatar Plugin
      <https://https://wiki.jenkins-ci.org/display/JENKINS/Avatar+Plugin>`_
      or the `Gravatar Plugin.
      <https://wiki.jenkins-ci.org/display/JENKINS/Gravatar+plugin>`_ or
      similar to set avatar picture for contributors.

    :arg bool show-changes: Show SCM change log for the first job in the
      pipeline. If Repository browser is configured, link to change will be
      created to the repository browser.

    :arg bool show-description: Show build description connected to a task.

    :arg bool show-promotions: Show promotions from the `Promoted Builds
      Plugin.
      <https://wiki.jenkins-ci.org/display/JENKINS/Promoted+Builds+Plugin>_`

    :arg bool show-total-buildtime: Show total build time of a pipeline.
      If there are multiple routes in a pipeline, total build time is
      calculated as the sum of the build times in the longest route.

    :arg str css-url: Possibility to override CSS for the normal view.
      Enter the full url to the custom CSS.

    :arg str fullscreen-css-url: Possibility to override CSS for the
      fullscreen view. Enter the full url to the custom CSS.

    :arg list regexp-first-jobs: Find jenkins job matching regular expression.
      ^build-(.+?)-project

    Example:

    .. literalinclude::  /../tests/views/fixtures/delivery_pipeline.yaml

    """
    delivery_pipeline = 'se.diabol.jenkins.pipeline.DeliveryPipelineView'

    view = XML.SubElement(xml_parent, delivery_pipeline)
    in_folder = data.get('folder', False)
    owner_attrs = dict()
    if in_folder:
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

    total_build_time = str(data.get('show-total-buildtime', False)).lower()
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
    XML.SubElement(view, 'fullScreenCss').text = data.get('csss-url')
    XML.SubElement(view, 'embeddedCss').text = data.get('fullscreen-csss-url')


def build_pipeline_view(parser, xml_parent, data):
    """
    Build Pipeline View requires the Jenkins `Build Pipeline Plugin.
    <https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin>`_


    :arg bool filter-executors: only those build executors will be shown that
      could execute the jobs in this view.
    :arg bool filter-queue: only jobs in this view will be shown in the queue.
    :arg bool folder: Wether or not this view is in a folder.
    :arg str name: The name of this view.
    :arg str first-job: Select the initial or parent Job in the build
                        pipeline view.
    :arg int display-number-of-builds: Select the number of build pipelines to
                                       display in the view.
    :arg str build-view-title: The title of this view.

    :arg str console-output-link-style: One the following:

        * **This Window**
        * **New Window**
        * **Light Box** (default)

    :arg bool trigger-only-latest-job: Select this option to restrict the
      display of a Trigger button to only the most recent successful build
      pipelines. This option will also limit retries to just unsuccessful
      builds of the most recent build pipelines.

      * **True**: Only the most recent successful builds displayed on the
                  view will have a manual trigger button for the next build
                  in the pipeline.
      * **False**: All successful builds displayed on the view will have a
                   manual trigger button for the next build in the pipeline.

    :arg bool always-allow-manual-trigger: Select this option if you want to
      be able to execute again a successful pipeline step. If the build is
      parameterized, this will re-execute the step using the same parameter
      values that were used when it was previously executed.

    :arg bool start-with-parameters: Select this option if you want to
      show the pipeline definition header in the pipeline view. If this option
      is not selected, then a pipeline that has never been run will not show
      any details about its jobs and appear like a blank form. Job details will
      only appear after the pipeline has been run at least once.

    :arg bool show-pipeline-parameters-in-header: Select this option if you
      want to display the parameters used to run the latest successful job
      in the pipeline's project headers.

    :arg bool show-pipeline-parameters: Select this option if you want to
      display the parameters used to run the first job in each pipeline's
      revision box.

    :arg bool refresh-frequency: Frequency at which the Build Pipeline
      Plugin updates the build cards in seconds

    :arg str css-url: Link to override style sheet

    Example:

    .. literalinclude::  /../tests/views/fixtures/build_pipeline_view.yaml
    """
    build_pipeline = 'au.com.centrumsystems.hudson.plugin.'\
                     'buildpipeline.BuildPipelineView'

    view = XML.SubElement(xml_parent, build_pipeline)

    in_folder = data.get('folder', False)
    owner_attrs = dict()
    if in_folder:
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
        'console-output-link-style', 'Light Box')

    if console_output_link_style not in console_output_links:
        raise ValueError('console-output-link-style must '
                         'be one of {}'.format(console_output_links))

    XML.SubElement(
        view, 'consoleOutputLinkStyle'
    ).text = console_output_link_style

    XML.SubElement(view, 'cssUrl').text = data.get('csss-url')

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

    start_with_params = str(data.get('start-with-parameters', False)).lower()
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
