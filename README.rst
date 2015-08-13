===============================
jenkins-job-builder-addons
===============================

.. image:: https://img.shields.io/travis/jimbydamonk/jenkins-job-builder-addons.svg
        :target: https://travis-ci.org/jimbydamonk/jenkins-job-builder-addons

.. image:: https://img.shields.io/pypi/v/jenkins-job-builder-addons.svg
        :target: https://pypi.python.org/pypi/jenkins-job-builder-addon



A set of addons for jenkins job builder

* Free software: Apache license
* Documentation: https://jenkins-job-builder-addons.readthedocs.org

Features
--------

* Supports job folders
* Supports Build Pipeline View
* Supports Delivery Pipeline View

Install
-------

* As of August 12th 2015 this requires two special branches. One for python-jenkins and one for jenkins-job-builder
1. Get python-jenkins  
  * git clone git://git.openstack.org/stackforge/python-jenkins
  * cd python-jenkins   
  * git fetch https://review.openstack.org/stackforge/python-jenkins refs/changes/85/180185/19 && git checkout 
  * python setup.py install
2. Get jenkins-job-builder 
  * git clone git://git.openstack.org/openstack-infra/jenkins-job-builder
  * cd jenksin-job-builder
  * git fetch https://review.openstack.org/openstack-infra/jenkins-job-builder refs/changes/07/134307/2 && git checkout FETCH_HEAD
  * python setup.py install

3. Get jenkins-job-builder-addons
  * git clone git@github.com:jimbydamonk/jenkins-job-builder-addons.git
  * cd jenkins-job-builder-addons 
  * python setup.py install 

