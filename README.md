## Aperte

**Aperte** is a lightweight data platform for membership-based communities.
It is slightly opinionated for volunteer-powered [SME](http://www.sme.org/)
chapters and communities, but it is customizable and can be adapted to various
other use cases.

### Motivation

Feedback and openness are essential ingredients for successful and engaging chapters.
Without these traits, members feel disconnected from the chapter leadership and
might resist participation in a chapter where they feel they have no voice
or clarity - understandably so.

The Internet is a powerful platform for collaboration and openness. Aperte is
an effort to provide a relatively convenient method for SME chapters to deploy an
open data platform for the benefit of membership and leaders alike.

### For Users.

TODO.

### For Developers.

#### Contributor Guidelines

Thank you for your consideration! Please review the project [Contributor Guidelines](.github/contributing.md).

#### Minimum Requirements

To work on this codebase, there are some minimum requirements that must be
available on your development machine.

- [Python 3](https://www.python.org/downloads/). Please note that Python 2.x is not supported.
- Fabric3 via `pip install Fabric3`. Ensure that Fabric**3** is installed here (with the 3 suffix). Fabric (without the suffix) will not work.
- [Docker CE](https://www.docker.com/community-edition).
- [Node.js version 8.0 or greater](https://nodejs.org/en/download/).
- [Yarn](https://yarnpkg.com/en/docs/install)

#### Fabric Commands

This codebase uses [Fabric](https://www.fabfile.org/) to manage the dependency
setup, project build process and Docker management.

| Command                          | Description                                                                                                                                                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fab init_dev`                   | **For a fresh clone, this command should be run first.** Set up the local machine development environment. An interactive wizard will ask some questions to set some environment variables that will be used during runtime. |
| `fab docker_setup`               | Run the interactive wizard again to set/change the environment variables used by a particular Docker environment.                                                                                                            |
| `fab docker_up:env=dev`          | Build and run the 'Local Docker Development' stack. Web application will be available at [http://www.lvh.me:8000](http://www.lvh.me:8000).                                                                                   |
| `fab docker_up:env=test`         | Build and run the 'Local Docker Testing' stack. Test results will appear in the Terminal or Command Line.                                                                                                                    |
| `fab docker_up:env=staging`      | Build and run the 'Local Docker Staging' stack. Web application will be available at [http://www.lvh.me:8000](http://www.lvh.me:8000).                                                                                       |
| `fab docker_destroy:env=dev`     | Stop the Docker stack, remove all containers and images created for the 'Local Docker Development' stack.                                                                                                                    |
| `fab docker_destroy:env=test`    | Stop the Docker stack, remove all containers and images created for the 'Local Docker Test' stack.                                                                                                                           |
| `fab docker_destroy:env=staging` | Stop the Docker stack, remove all containers and images created for the 'Local Docker Staging' stack.                                                                                                                        |
| `fab deploy_setup`               | Run an interactive wizard to set/change the environment variables used by a particular GAE deployment.                                                                                                                       |
| `fab deploy:env=staging`         | Deploy web application to Google App Engine staging target.                                                                                                                                                                  |
| `fab deploy:env=prod`            | Deploy web application to Google App Engine production target.                                                                                                                                                               |

#### Runtime Environments

This project supports a variety of runtime environments - both locally and in
the Cloud.

For local development/staging environments, Docker is utilized so that any
development and testing is performed in a reproducible environment on different
machines.

The Docker images that are built to closely resemble the Google App Engine
deployment target.

For cloud staging/production environments, the Aperte deployment scripts support
the [Google App Engine Standard Environment](https://cloud.google.com/appengine/docs/standard/python3/)
out of the box.

That said, the codebase is Cloud-agnostic so there is nothing to prevent it from
running on other Cloud providers.

| Name                        | Description                                                                                                                                                                  |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local Docker Development    | Runs Django in Debug mode, start a local HTTP server and automatically refresh the web application after each source change.                                                 |
| Local Docker Testing        | Runs the full set of integration and unit tests for the front and back ends.                                                                                                 |
| Local Docker Staging        | Runs Django with settings that mimic the production environment as close as possible. A local HTTP server will be started but it will not refresh if changes are made.       |
| GAE Staging                 | Runs on a Google App Engine environment (that is separate from Production) for QA using Django staging settings and actual Google Cloud Platform resources (i.e. Cloud SQL). |
| GAE Production              | For actual customer/member traffic.                                                                                                                                          |
| Continuous Integration (CI) | For [Circle CI](https://circleci.com/) automated integration testing at commit.                                                                                              |

### Community Participation Guidelines

The SME Virtual Network is committed to providing a friendly, safe and welcoming
environment for all. Please take a moment to read our
[Community Participation Guidelines](https://github.com/smevirtual/community-guidelines/blob/master/README.md).

### License

All of the code in this repository is licensed under the
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/). A copy of this license
is included in the root of this repository.

At times, there might be other source code incorporated into Aperte which carry
different open-source licenses, where those instances occur, notations will be
made in the headers of effected source files and/or the original source code
licenses will be included in close proximity to these files.
