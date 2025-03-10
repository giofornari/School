FROM php:8-apache

RUN apt update -y && docker-php-ext-install mysqli && docker-php-ext-enable mysqli
RUN a2enmod rewrite

COPY src /var/www/html/
