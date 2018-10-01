"""
Views show job status.

**Component**: views
  :Macro: views
  :Entry Point: jenkins_jobs.views
"""

import logging

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base

import jenkins_jobs.modules.helpers as helpers

logger = logging.getLogger(__name__)


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

    parent = data.get('parent', False)
    if parent:
        clazz = 'com.cloudbees.hudson.plugins.folder.Folder'
        if ("nested-view" == parent):
            clazz = 'hudson.plugins.nested_view.NestedView'
        elif ("list-view" == parent):
            clazz = 'hudson.model.ListView'
        owner_attrs = dict()
        owner_attrs['class'] = clazz
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    logger.debug("Read parent '{0}' to '{1}'".format(parent, data.get('name')))

    executors = data.get('filter-executors', False)
    XML.SubElement(view, 'filterExecutors').text = str(executors).lower()

    queue = data.get('filter-queue', False)
    XML.SubElement(view, 'filterQueue').text = str(queue).lower()

    properties_attributes = dict()
    properties_attributes['class'] = 'hudson.model.View$PropertyList'
    XML.SubElement(view, 'properties', attrib=properties_attributes)


def workflow_pipeline_view(parser, xml_parent, data):
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
    :arg int number-of-columns: Number of columns used for showing pipelines.
                                Useful for multiple components in the view to
                                show them beside each others.

    :arg int sorting: How to sort the pipeline in the view.
                      Only applicable for several pipelines.
                      Can be sorted by latest activity or by name.
    :arg int update-interval: How often will the view be updated in seconds.

    :arg bool allow-pipeline-start: Start a new pipeline build.

    :arg bool show-changes: Show SCM change log for the first job in the
      pipeline. If Repository browser is configured, link to change will be
      created to the repository browser.

    :arg list regexp-first-jobs: Find jenkins job matching regular expression.
      ^build-(.+?)-project

    Example:

    .. literalinclude::  /../tests/views/fixtures/delivery_pipeline.yaml

    """
    delivery_pipeline = 'se.diabol.jenkins.workflow.WorkflowPipelineView'

    view = XML.SubElement(xml_parent, delivery_pipeline)

    parent = data.get('parent', False)
    if parent:
        clazz = 'com.cloudbees.hudson.plugins.folder.Folder'
        if ("nested-view" == parent):
            clazz = 'hudson.plugins.nested_view.NestedView'
        elif ("list-view" == parent):
            clazz = 'hudson.model.ListView'
        owner_attrs = dict()
        owner_attrs['class'] = clazz
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    logger.debug("Read parent '{0}' to '{1}'".format(parent, data.get('name')))

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
        spec_class = "se.diabol.jenkins.workflow."\
                     "WorkflowPipelineView_-ComponentSpec"
        component_spec = XML.SubElement(xml_components, spec_class)
        name = component.get('name')
        XML.SubElement(component_spec, 'name').text = name
        first_job = component.get('job')
        XML.SubElement(component_spec, 'job').text = first_job

    number_of_pipelines = str(data.get('number-of-pipelines', 3))
    XML.SubElement(
        view, 'noOfPipelines').text = number_of_pipelines

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

    update_interval = str(data.get('update-interval', 1))
    XML.SubElement(view, 'updateInterval').text = update_interval

    show_changes = str(data.get('show-changes', False)).lower()
    XML.SubElement(view, 'showChanges').text = str(show_changes).lower()

    pipeline_start = str(data.get('allow-pipeline-start', False)).lower()
    XML.SubElement(view, 'allowPipelineStart').text = pipeline_start


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

    parent = data.get('parent', False)
    if parent:
        clazz = 'com.cloudbees.hudson.plugins.folder.Folder'
        if ("nested-view" == parent):
            clazz = 'hudson.plugins.nested_view.NestedView'
        elif ("list-view" == parent):
            clazz = 'hudson.model.ListView'
        owner_attrs = dict()
        owner_attrs['class'] = clazz
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    logger.debug("Read parent '{0}' to '{1}'".format(parent, data.get('name')))

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

    parent = data.get('parent', False)
    if parent:
        clazz = 'com.cloudbees.hudson.plugins.folder.Folder'
        if ("nested-view" == parent):
            clazz = 'hudson.plugins.nested_view.NestedView'
        elif ("list-view" == parent):
            clazz = 'hudson.model.ListView'
        owner_attrs = dict()
        owner_attrs['class'] = clazz
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    logger.debug("Read parent '{0}' to '{1}'".format(parent, data.get('name')))

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


def nested_view(parser, xml_parent, data):
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

    COLUMN_DICT = {
        'status': 'hudson.views.StatusColumn',
        'weather': 'hudson.views.WeatherColumn',
    }
    DEFAULT_COLUMNS = ['status', 'weather']

    delivery_pipeline = 'hudson.plugins.nested_view.NestedView'

    view = XML.SubElement(xml_parent, delivery_pipeline)

    XML.SubElement(view, 'name').text = data.get('name')
    XML.SubElement(view, 'description').text = data.get('description', None)

    parent = data.get('parent', False)
    if parent:
        clazz = 'com.cloudbees.hudson.plugins.folder.Folder'
        if ("nested-view" == parent):
            clazz = 'hudson.plugins.nested_view.NestedView'
        elif ("list-view" == parent):
            clazz = 'hudson.model.ListView'
        owner_attrs = dict()
        owner_attrs['class'] = clazz
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    logger.debug("Read parent '{0}' to '{1}'".format(parent, data.get('name')))

    executors = data.get('filter-executors', False)
    XML.SubElement(view, 'filterExecutors').text = str(executors).lower()

    queue = data.get('filter-queue', False)
    XML.SubElement(view, 'filterQueue').text = str(queue).lower()

    defaultView = data.get('default-view', None)
    XML.SubElement(view, 'defaultView').text = defaultView

    XML.SubElement(view, 'views')

    c_xml = None
    if ("nested-view" == parent):
        c_xml = XML.SubElement(view, 'columns')
        c_xml = XML.SubElement(c_xml, 'columns')
    else:
        c_xml = XML.SubElement(view, 'columns')

    columns = data.get('columns', DEFAULT_COLUMNS)

    for column in columns:
        if isinstance(column, dict):
            if 'extra-build-parameter' in column:
                p_name = column['extra-build-parameter']
                x = XML.SubElement(
                    c_xml,
                    'jenkins.plugins.extracolumns.BuildParametersColumn',
                    plugin='extra-columns'
                )
                x.append(XML.fromstring(
                    '<singlePara>true</singlePara>'))
                x.append(XML.fromstring(
                    '<parameterName>%s</parameterName>' % p_name))
        else:
            if column in COLUMN_DICT:
                if isinstance(COLUMN_DICT[column], list):
                    x = XML.SubElement(c_xml, COLUMN_DICT[column][0][0],
                                       **COLUMN_DICT[column][0][1])
                    for tag in COLUMN_DICT[column][1:]:
                        x.append(XML.fromstring(tag))
                else:
                    XML.SubElement(c_xml, COLUMN_DICT[column])


def sublist_view(parser, xml_parent, data):

    COLUMN_DICT = {
        'status': 'hudson.views.StatusColumn',
        'weather': 'hudson.views.WeatherColumn',
        'job': 'hudson.views.JobColumn',
        'last-success': 'hudson.views.LastSuccessColumn',
        'last-failure': 'hudson.views.LastFailureColumn',
        'last-duration': 'hudson.views.LastDurationColumn',
        'build-button': 'hudson.views.BuildButtonColumn',
        'last-stable': 'hudson.views.LastStableColumn',
        'robot-list': 'hudson.plugins.robot.view.RobotListViewColumn',
        'find-bugs': 'hudson.plugins.findbugs.FindBugsColumn',
        'jacoco': 'hudson.plugins.jacococoveragecolumn.JaCoCoColumn',
        'git-branch': 'hudson.plugins.git.GitBranchSpecifierColumn',
        'schedule-build':
            'org.jenkinsci.plugins.schedulebuild.ScheduleBuildButtonColumn',
        'priority-sorter': 'jenkins.advancedqueue.PrioritySorterJobColumn',
        'build-filter': 'hudson.views.BuildFilterColumn',
        'desc': 'jenkins.branch.DescriptionColumn',
        'policy-violations':
            'com.sonatype.insight.ci.hudson.QualityColumn '
            'plugin="sonatype-clm-ci"',
        'member-graph-view':
            'com.barchart.jenkins.cascade.GraphViewColumn '
            'plugin="maven-release-cascade"',
        'extra-tests-total': [
            ['jenkins.plugins.extracolumns.TestResultColumn',
             {'plugin': 'extra-columns'}],
            '<testResultFormat>2</testResultFormat>'],
        'extra-tests-failed': [
            ['jenkins.plugins.extracolumns.TestResultColumn',
             {'plugin': 'extra-columns'}],
            '<testResultFormat>3</testResultFormat>'],
        'extra-tests-passed': [
            ['jenkins.plugins.extracolumns.TestResultColumn',
             {'plugin': 'extra-columns'}],
            '<testResultFormat>4</testResultFormat>'],
        'extra-tests-skipped': [
            ['jenkins.plugins.extracolumns.TestResultColumn',
             {'plugin': 'extra-columns'}],
            '<testResultFormat>5</testResultFormat>'],
        'extra-tests-format-0': [
            ['jenkins.plugins.extracolumns.TestResultColumn',
             {'plugin': 'extra-columns'}],
            '<testResultFormat>0</testResultFormat>'],
        'extra-tests-format-1': [
            ['jenkins.plugins.extracolumns.TestResultColumn',
             {'plugin': 'extra-columns'}],
            '<testResultFormat>1</testResultFormat>'],
        'extra-build-description': [
            ['jenkins.plugins.extracolumns.BuildDescriptionColumn',
             {'plugin': 'extra-columns'}],
            '<columnWidth>3</columnWidth>', '<forceWidth>false</forceWidth>'],
        'extra-build-parameters': [
            ['jenkins.plugins.extracolumns.BuildParametersColumn',
             {'plugin': 'extra-columns'}],
            '<singlePara>false</singlePara>', '<parameterName/>'],
        'extra-last-user-name':
            'jenkins.plugins.extracolumns.UserNameColumn'
            ' plugin="extra-columns"',
        'extra-last-output':
            'jenkins.plugins.extracolumns.LastBuildConsoleColumn'
            ' plugin="extra-columns"',
        'extra-workspace-link':
            'jenkins.plugins.extracolumns.WorkspaceColumn '
            'plugin="extra-columns"',
        'extra-configure-button':
            'jenkins.plugins.extracolumns.ConfigureProjectColumn'
            ' plugin="extra-columns"',
    }
    DEFAULT_COLUMNS = ['status', 'weather', 'job', 'last-success',
        'last-failure', 'last-duration', 'build-button']


    #view = XML.Element('hudson.model.ListView')
    view = XML.SubElement(xml_parent, 'hudson.model.ListView')

    mapping = [
        ('name', 'name', None),
        ('description', 'description', ''),
        ('filter-executors', 'filterExecutors', False),
        ('filter-queue', 'filterQueue', False),
    ]
            
    helpers.convert_mapping_to_xml(view, data, mapping, fail_required=True)

    parent = data.get('parent', False)
    if parent:
        clazz = 'com.cloudbees.hudson.plugins.folder.Folder'
        if ("nested-view" == parent):
            clazz = 'hudson.plugins.nested_view.NestedView'
        elif ("list-view" == parent):
            clazz = 'hudson.model.ListView'
        owner_attrs = dict()
        owner_attrs['class'] = clazz
        owner_attrs['reference'] = '../../..'
        XML.SubElement(view, 'owner', attrib=owner_attrs)

    logger.debug("Read parent '{0}' to '{1}'".format(parent, data.get('name')))

    XML.SubElement(view, 'properties',
                   {'class': 'hudson.model.View$PropertyList'})

    jn_xml = XML.SubElement(view, 'jobNames')
    jobnames = data.get('job-name', None)
    XML.SubElement(
        jn_xml,
        'comparator', {
            'class': 'hudson.util.CaseInsensitiveComparator'
        }
    )
    if jobnames is not None:
        # Job names must be sorted in the xml
        jobnames = sorted(jobnames, key=str.lower)
        for jobname in jobnames:
            XML.SubElement(jn_xml, 'string').text = str(jobname)

    job_filter_xml = XML.SubElement(view, 'jobFilters')
    jobfilters = data.get('job-filters', [])

    for jobfilter in jobfilters:
        if jobfilter == 'most-recent':
            mr_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.MostRecentJobsFilter')
            mr_xml.set('plugin', 'view-job-filters')
            mr_data = jobfilters.get('most-recent')
            mapping = [
                ('max-to-include', 'maxToInclude', '0'),
                ('check-start-time', 'checkStartTime', False),
            ]
            helpers.convert_mapping_to_xml(mr_xml, mr_data, mapping,
                                   fail_required=True)

        if jobfilter == 'build-duration':
            bd_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.BuildDurationFilter')
            bd_xml.set('plugin', 'view-job-filters')
            bd_data = jobfilters.get('build-duration')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('build-duration-type', 'buildCountTypeString', 'Latest'),
                ('amount-type', 'amountTypeString', 'Hours'),
                ('amount', 'amount', '0'),
                ('less-than', 'lessThan', True),
                ('build-duration-minutes', 'buildDurationMinutes', '0'),
            ]
            helpers.convert_mapping_to_xml(bd_xml, bd_data, mapping,
                                   fail_required=True)

        if jobfilter == 'build-trend':
            bt_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.BuildTrendFilter')
            bt_xml.set('plugin', 'view-job-filters')
            bt_data = jobfilters.get('build-trend')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('build-trend-type', 'buildCountTypeString', 'Latest'),
                ('amount-type', 'amountTypeString', 'Hours'),
                ('amount', 'amount', '0'),
                ('status', 'statusTypeString', 'Completed'),
            ]
            helpers.convert_mapping_to_xml(bt_xml, bt_data, mapping,
                                   fail_required=True)

        if jobfilter == 'job-status':
            js_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.JobStatusFilter')
            js_xml.set('plugin', 'view-job-filters')
            js_data = jobfilters.get('job-status')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('unstable', 'unstable', False),
                ('failed', 'failed', False),
                ('aborted', 'aborted', False),
                ('disabled', 'disabled', False),
                ('stable', 'stable', False),
            ]
            helpers.convert_mapping_to_xml(js_xml, js_data, mapping,
                                   fail_required=True)

        if jobfilter == 'upstream-downstream':
            ud_xml = XML.SubElement(
                job_filter_xml,
                'hudson.views.UpstreamDownstreamJobsFilter'
            )
            ud_xml.set('plugin', 'view-job-filters')
            ud_data = jobfilters.get('upstream-downstream')
            mapping = [
                ('include-upstream', 'includeUpstream',
                 False),
                ('include-downstream', 'includeDownstream', False),
                ('recursive', 'recursive', False),
                ('exclude-originals', 'excludeOriginals', False),
            ]
            helpers.convert_mapping_to_xml(ud_xml, ud_data, mapping,
                                   fail_required=True)

        if jobfilter == 'fallback':
            fb_xml = XML.SubElement(
                job_filter_xml,
                'hudson.views.AddRemoveFallbackFilter'
            )
            fb_xml.set('plugin', 'view-job-filters')
            fb_data = jobfilters.get('fallback')
            mapping = [
                ('fallback-type', 'fallbackTypeString',
                 'REMOVE_ALL_IF_ALL_INCLUDED'),
                ('fallback-type', 'fallbackType',
                 'REMOVE_ALL_IF_ALL_INCLUDED'),
            ]
            helpers.convert_mapping_to_xml(fb_xml, fb_data, mapping,
                                   fail_required=True)

        if jobfilter == 'build-status':
            bs_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.BuildStatusFilter')
            bs_xml.set('plugin', 'view-job-filters')
            bs_data = jobfilters.get('build-status')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('never-built', 'neverBuilt', False),
                ('building', 'building', False),
                ('in-build-queue', 'inBuildQueue', False),
            ]
            helpers.convert_mapping_to_xml(bs_xml, bs_data, mapping,
                                   fail_required=True)

        if jobfilter == 'user-relevence':
            ur_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.UserRelevanceFilter')
            ur_xml.set('plugin', 'view-job-filters')
            ur_data = jobfilters.get('user-relevence')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('build-count', 'buildCountTypeString', 'AtLeastOne'),
                ('amount-type', 'amountTypeString', 'Hours'),
                ('amount', 'amount', '0'),
                ('match-user-id', 'matchUserId', False),
                ('match-user-fullname', 'matchUserFullName', False),
                ('ignore-case', 'ignoreCase', False),
                ('ignore-whitespace', 'ignoreWhitespace', False),
                ('ignore-non-alphaNumeric', 'ignoreNonAlphaNumeric',
                 False),
                ('match-builder', 'matchBuilder', False),
                ('match-email', 'matchEmail', False),
                ('match-scm-changes', 'matchScmChanges', False),
            ]
            helpers.convert_mapping_to_xml(ur_xml, ur_data, mapping,
                                   fail_required=True)

        if jobfilter == 'regex-job':
            rj_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.RegExJobFilter')
            rj_xml.set('plugin', 'view-job-filters')
            rj_data = jobfilters.get('regex-job')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('regex-name', 'valueTypeString', ''),
                ('regex', 'regex', ''),
            ]
            helpers.convert_mapping_to_xml(rj_xml, rj_data, mapping,
                                   fail_required=True)

        if jobfilter == 'job-type':
            jt_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.JobTypeFilter')
            jt_xml.set('plugin', 'view-job-filters')
            jt_data = jobfilters.get('job-type')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('job-type', 'jobType', 'hudson.model.FreeStyleProject'),
            ]
            helpers.convert_mapping_to_xml(jt_xml, jt_data, mapping,
                                   fail_required=True)

        if jobfilter == 'parameter':
            pr_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.ParameterFilter')
            pr_xml.set('plugin', 'view-job-filters')
            pr_data = jobfilters.get('parameter')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('name', 'nameRegex', ''),
                ('value', 'valueRegex', ''),
                ('description', 'descriptionRegex', ''),
                ('use-default', 'useDefaultValue', False),
                ('match-builds-in-progress', 'matchBuildsInProgress',
                 False),
                ('match-all-builds', 'matchAllBuilds', False),
                ('max-builds-to-match', 'maxBuildsToMatch', 0),
            ]
            helpers.convert_mapping_to_xml(pr_xml, pr_data, mapping,
                                   fail_required=True)

        if jobfilter == 'other-views':
            ov_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.OtherViewsFilter')
            ov_xml.set('plugin', 'view-job-filters')
            ov_data = jobfilters.get('other-views')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('view-name', 'otherViewName',
                 '&lt;select a view other than this one&gt;'),
            ]
            helpers.convert_mapping_to_xml(ov_xml, ov_data, mapping,
                                   fail_required=True)

        if jobfilter == 'scm':
            st_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.ScmTypeFilter')
            st_xml.set('plugin', 'view-job-filters')
            st_data = jobfilters.get('scm')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('scm-type', 'scmType', 'hudson.scm.NullSCM'),
            ]
            helpers.convert_mapping_to_xml(st_xml, st_data, mapping,
                                   fail_required=True)

        if jobfilter == 'secured-job':
            sj_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.SecuredJobsFilter')
            sj_xml.set('plugin', 'view-job-filters')
            sj_data = jobfilters.get('secured-job')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
            ]
            helpers.convert_mapping_to_xml(sj_xml, sj_data, mapping,
                                   fail_required=True)

        if jobfilter == 'user-permissions':
            up_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.SecurityFilter')
            up_xml.set('plugin', 'view-job-filters')
            up_data = jobfilters.get('user-permissions')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
                ('configure', 'configure', False),
                ('build', 'build', False),
                ('workspace', 'workspace', False),
                ('permission-check', 'permissionCheckType',
                 'MustMatchAll'),
            ]
            helpers.convert_mapping_to_xml(up_xml, up_data, mapping,
                                   fail_required=True)

        if jobfilter == 'unclassified':
            uc_xml = XML.SubElement(job_filter_xml,
                                    'hudson.views.UnclassifiedJobsFilter')
            uc_xml.set('plugin', 'view-job-filters')
            uc_data = jobfilters.get('unclassified')
            mapping = [
                ('match-type', 'includeExcludeTypeString',
                 'includeMatched'),
            ]
            helpers.convert_mapping_to_xml(uc_xml, uc_data, mapping,
                                   fail_required=True)

    c_xml = None
    if ("nested-view" == parent):
        c_xml = XML.SubElement(view, 'columns')
        c_xml = XML.SubElement(c_xml, 'columns')
    else:
        c_xml = XML.SubElement(view, 'columns')

    columns = data.get('columns', DEFAULT_COLUMNS)

    for column in columns:
        if isinstance(column, dict):
            if 'extra-build-parameter' in column:
                p_name = column['extra-build-parameter']
                x = XML.SubElement(
                    c_xml,
                    'jenkins.plugins.extracolumns.BuildParametersColumn',
                    plugin='extra-columns'
                )
                x.append(XML.fromstring(
                    '<singlePara>true</singlePara>'))
                x.append(XML.fromstring(
                    '<parameterName>%s</parameterName>' % p_name))
        else:
            if column in COLUMN_DICT:
                if isinstance(COLUMN_DICT[column], list):
                    x = XML.SubElement(c_xml, COLUMN_DICT[column][0][0],
                                       **COLUMN_DICT[column][0][1])
                    for tag in COLUMN_DICT[column][1:]:
                        x.append(XML.fromstring(tag))
                else:
                    XML.SubElement(c_xml, COLUMN_DICT[column])
    mapping = [
        ('regex', 'includeRegex', None),
        ('recurse', 'recurse', False),
        ('status-filter', 'statusFilter', None),
    ]
    helpers.convert_mapping_to_xml(
        view, data, mapping, fail_required=False)


class NestedRoot(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):

        COLUMN_DICT = {
            'status': 'hudson.views.StatusColumn',
            'weather': 'hudson.views.WeatherColumn',
        }
        DEFAULT_COLUMNS = ['status', 'weather']

        root = XML.Element('hudson.plugins.nested_view.NestedView',
                           {'plugin': 'nested-view'})

        XML.SubElement(root, 'name').text = data.get('name')
        XML.SubElement(root, 'description').text = data.get('description', None)

        executors = data.get('filter-executors', False)
        XML.SubElement(root, 'filterExecutors').text = str(executors).lower()

        queue = data.get('filter-queue', False)
        XML.SubElement(root, 'filterQueue').text = str(queue).lower()

        defaultView = data.get('default-view', None)
        XML.SubElement(root, 'defaultView').text = defaultView

        XML.SubElement(root, 'views')

        c_xml = c_xml = XML.SubElement(root, 'columns')
        c_xml = XML.SubElement(c_xml, 'columns')

        columns = data.get('columns', DEFAULT_COLUMNS)

        for column in columns:
            if isinstance(column, dict):
                if 'extra-build-parameter' in column:
                    p_name = column['extra-build-parameter']
                    x = XML.SubElement(
                        c_xml,
                        'jenkins.plugins.extracolumns.BuildParametersColumn',
                        plugin='extra-columns'
                    )
                    x.append(XML.fromstring(
                        '<singlePara>true</singlePara>'))
                    x.append(XML.fromstring(
                        '<parameterName>%s</parameterName>' % p_name))
            else:
                if column in COLUMN_DICT:
                    if isinstance(COLUMN_DICT[column], list):
                        x = XML.SubElement(c_xml, COLUMN_DICT[column][0][0],
                                           **COLUMN_DICT[column][0][1])
                        for tag in COLUMN_DICT[column][1:]:
                            x.append(XML.fromstring(tag))
                    else:
                        XML.SubElement(c_xml, COLUMN_DICT[column])

        return root


class Views(jenkins_jobs.modules.base.Base):
    sequence = 20

    component_type = 'view'
    component_list_type = 'views'

    def gen_xml(self, xml_parent, data):
        views = XML.SubElement(xml_parent, 'views')

        for view in data.get('views', []):

            if isinstance(view, dict):
                template_name, view_data = next(iter(view.items()))
                if not isinstance(view_data, dict):
                    view_data = {}
            else:
                continue

            view_data = self.registry.parser._applyDefaults(view_data)
            views_data = []

            template = self.registry.parser._getViewTemplate(template_name)
            if template:
                d = type(view_data)(view_data)
                d['views'] = []
                views_data = self.registry.parser._expandYamlForTemplateView(d,
                    template)
            else:
                view_data['name'] = self.registry.parser._getfullname(view_data)
                logger.debug("Expanding view '{0}'".format(view_data['name']))
                self.registry.parser._formatDescription(view_data)
                #self.registry.parser.views.append(view)
                views_data.append(view_data)

            for v_data in views_data:

                dict_view = {}

                dict_view[v_data.get('view-type', template_name)] = v_data

                logger.debug("reading view node on '{0}' - '{1}'".format(
                    v_data.get('view-type', template_name), dict_view))

                self.registry.dispatch('view', views, dict_view)
