# Calico
[![Build](https://img.shields.io/github/actions/workflow/status/jacobmonck/calico/docker-image.yml?style=for-the-badge)](https://github.com/JacobMonck/calico/actions/workflows/docker-image.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge&logo=black.svg)](https://github.com/psf/black)
<img src="assets/gtao-dashboard.png">

## What is it?

Calico is an advanced metrics collection and dataproccessing tool designed for large Discord communities.

This project started as an internal tool for the GTA Online Discord community which consists of over 500k members. We wanted an easy and clean way to gather and display server information. Eventually as I was the only one working on the project I decided to make it open source and use it as a portfolio project.

# Table of contents
1. [Features](#features)
2. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Using the default Docker Compose](#using-the-default-docker-compose)
3. [License](#license)

## Features
- Reaction satastics
- Message statstics
- Member count statistics
- Automaticaly synchronizes with your guild

## Installation

### Prerequisites

- Docker
- Linux Server

### Using the default Docker Compose

The default Docker Compose includes the bot, a Postgres instance, and a Metabase instance exposed on port 3000.

1. Create a `.env` and `.config.yml` file using the `.env.example` and `config-example.yml` as reference.
2. `$ docker compose up --build`
3. Add metabase to your domain/webserver (Metabase runs on port 3000)


## License

You may use and redistribute this software as long as you follow the Elastic License 2.0 (ELv2)
