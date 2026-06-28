#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import socket

from shadowsocks import common


OUTBOUND_IPV4 = 'ipv4'
OUTBOUND_IPV6 = 'ipv6'


def _to_str(value):
    if value is None:
        return ''
    return common.to_str(value)


def normalize_domain(domain):
    domain = _to_str(domain).strip().lower()
    if domain.endswith('.'):
        domain = domain[:-1]
    return domain


def match_domain_suffix(hostname, suffix):
    hostname = normalize_domain(hostname)
    suffix = normalize_domain(suffix)
    if not hostname or not suffix:
        return False
    return hostname == suffix or hostname.endswith('.' + suffix)


def match_domain_keyword(hostname, keyword):
    hostname = normalize_domain(hostname)
    keyword = normalize_domain(keyword)
    if not hostname or not keyword:
        return False
    return keyword in hostname


def _outbound_to_family(outbound):
    outbound = normalize_domain(outbound)
    if outbound == OUTBOUND_IPV4:
        return socket.AF_INET
    if outbound == OUTBOUND_IPV6:
        return socket.AF_INET6
    return None


def _family_to_outbound(family):
    if family == socket.AF_INET:
        return OUTBOUND_IPV4
    if family == socket.AF_INET6:
        return OUTBOUND_IPV6
    return None


def _ip_outbound(hostname):
    family = common.is_ip(hostname)
    if family:
        return _family_to_outbound(family)
    return None


def _as_list(value):
    value = value or []
    if not isinstance(value, list):
        value = [value]
    return value


def _make_route(rule):
    return {
        'name': rule.get('name', ''),
        'outbound': normalize_domain(rule.get('outbound', OUTBOUND_IPV4)),
        'fallback': normalize_domain(rule.get('fallback', '')),
        'matched': True
    }


def get_route(config, hostname):
    ip_outbound = _ip_outbound(hostname)
    if ip_outbound:
        return {
            'name': 'ip-literal',
            'outbound': ip_outbound,
            'fallback': None,
            'matched': False
        }

    rules = config.get('route_rules', []) or []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        for domain in _as_list(rule.get('domains', [])):
            if match_domain_suffix(hostname, domain):
                return _make_route(rule)
        for keyword in _as_list(rule.get('domain_keywords', [])):
            if match_domain_keyword(hostname, keyword):
                return _make_route(rule)

    default_outbound = normalize_domain(config.get('default_outbound', ''))
    if default_outbound:
        return {
            'name': 'default',
            'outbound': default_outbound,
            'fallback': None,
            'matched': False
        }

    return {
        'name': 'legacy',
        'outbound': None,
        'fallback': None,
        'matched': False
    }


def get_route_family(route):
    return _outbound_to_family(route.get('outbound'))


def get_fallback_family(route):
    fallback = route.get('fallback')
    if not fallback:
        return None
    if fallback == route.get('outbound'):
        return None
    return _outbound_to_family(fallback)
