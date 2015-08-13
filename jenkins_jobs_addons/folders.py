"""
The Folder plugin handles creating CloudBeesFolder Jenkins Jobs.
You man specify ``folder`` in the ``project-type`` attribute of the
:ref:`Job` definition.

Requires the Jenkins `CloudBees Folder Plugin.
<CloudBees+Folder+Plugin>`_

    :arg str primary-view: Name of the default view to show for this folder.
    :arg list health-metrics: A list of metrics to use as a health check. Must
      be one of the following:
        * **worst-child-health-metric**

Job example:

    .. literalinclude::
      /../tests/folders/fixtures/folders.yaml

"""

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base

FOLDER_CLASS = 'com.cloudbees.hudson.plugins.folder.Folder'
METRIC_CLASS = 'com.cloudbees.hudson.plugins.folder.health.'\
               'WorstChildHealthMetric'
STOCK_FOLDER_ICON = 'com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon'
SUPPORTED_METRICS = {
    'worst-child-health-metric':
    'com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric'
}


class Folder(jenkins_jobs.modules.base.Base):

    """
    Class built off :ref:`Base`
    """
    sequence = 0

    def root_xml(self, data):
        """
        Called after data is parsed.
        Returns xml representing a job
        :arg dict data: the YAML data structure
        """
        xml_parent = XML.Element(FOLDER_CLASS)
        XML.SubElement(xml_parent, 'icon', attrib={'class': STOCK_FOLDER_ICON})

        health_metrics = data.get('health-metrics', [])
        metrics = XML.SubElement(xml_parent, 'healthMetrics')
        for health_metric in health_metrics:
            if health_metric in SUPPORTED_METRICS.keys():
                XML.SubElement(metrics, SUPPORTED_METRICS.get(health_metric))

        primary_view = data.get('primary-view')
        XML.SubElement(xml_parent, 'primaryView').text = primary_view
        return xml_parent
