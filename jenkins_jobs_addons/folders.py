"""
The Folder plugin handles creating CloudBeesFolder Jenkins Jobs.
You man specify ``folder`` in the ``project-type`` attribute of the
:ref:`Job` definition.
"""

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base

FOLDER_CLASS = 'com.cloudbees.hudson.plugins.folder.Folder'
METRIC_CLASS = 'com.cloudbees.hudson.plugins.folder.health.'\
               'WorstChildHealthMetric'
STOCK_FOLDER_ICON = 'com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon'


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

        health_metrics = bool(data.get('health-metrics', False))
        metric = XML.SubElement(xml_parent, 'healthMetrics')
        if health_metrics:
            XML.SubElement(metric, METRIC_CLASS)

        return xml_parent
