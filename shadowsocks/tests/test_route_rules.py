#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import socket
import sys
import unittest

if __name__ == '__main__':
    file_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.join(file_path, '../'))

from shadowsocks import common, router


class RouteRuleTest(unittest.TestCase):

    def test_domain_suffix_match(self):
        self.assertTrue(router.match_domain_suffix('google.com', 'google.com'))
        self.assertTrue(router.match_domain_suffix('www.google.com',
                                                   'google.com'))
        self.assertTrue(router.match_domain_suffix('WWW.GOOGLE.COM.',
                                                   'google.com'))
        self.assertFalse(router.match_domain_suffix('badgoogle.com',
                                                    'google.com'))

    def test_domain_keyword_match(self):
        self.assertTrue(router.match_domain_keyword('www.google.com',
                                                    'google'))
        self.assertTrue(router.match_domain_keyword('googleapis.com',
                                                    'google'))
        self.assertTrue(router.match_domain_keyword('notgoogle.com',
                                                    'google'))
        self.assertTrue(router.match_domain_keyword('WWW.GOOGLE.COM.',
                                                    'google'))
        self.assertFalse(router.match_domain_keyword('', 'google'))
        self.assertFalse(router.match_domain_keyword('www.google.com', ''))

    def test_route_rule_prefers_ipv6(self):
        config = {
            'default_outbound': 'ipv4',
            'route_rules': [{
                'name': 'google-ipv6',
                'domains': ['google.com'],
                'outbound': 'ipv6',
                'fallback': 'ipv4'
            }]
        }
        route = router.get_route(config, b'www.google.com')
        self.assertEqual(socket.AF_INET6, router.get_route_family(route))
        self.assertEqual(socket.AF_INET, router.get_fallback_family(route))

    def test_route_rule_domain_keyword_prefers_ipv6(self):
        config = {
            'default_outbound': 'ipv4',
            'route_rules': [{
                'name': 'google-keyword-ipv6',
                'domain_keywords': ['google'],
                'outbound': 'ipv6',
                'fallback': 'ipv4'
            }]
        }
        route = router.get_route(config, b'googleapis.com')
        self.assertEqual(socket.AF_INET6, router.get_route_family(route))
        self.assertEqual(socket.AF_INET, router.get_fallback_family(route))

    def test_default_route_uses_ipv4(self):
        config = {
            'default_outbound': 'ipv4',
            'route_rules': []
        }
        route = router.get_route(config, b'example.com')
        self.assertEqual(socket.AF_INET, router.get_route_family(route))
        self.assertIsNone(router.get_fallback_family(route))


class DNSCacheKeyTest(unittest.TestCase):

    def test_cache_key_separates_address_families(self):
        remote_addr = (b'example.com', 443)
        handler = common.UDPAsyncDNSHandler(())
        self.assertNotEqual(handler._cache_key(remote_addr, socket.AF_INET),
                            handler._cache_key(remote_addr, socket.AF_INET6))
        self.assertNotEqual(handler._cache_key(remote_addr, None),
                            handler._cache_key(remote_addr, socket.AF_INET))


if __name__ == '__main__':
    unittest.main()
