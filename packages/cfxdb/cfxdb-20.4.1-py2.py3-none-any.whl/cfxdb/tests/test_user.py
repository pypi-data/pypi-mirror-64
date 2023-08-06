##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import os
import uuid
import binascii
from datetime import datetime

import pytest
import cbor
import flatbuffers

from autobahn import util
import txaio

from cfxdb.user import User, UserFbs
from cfxdb.user import ActivationToken, ActivationTokenFbs
from cfxdb.user import Organization, OrganizationFbs

txaio.use_twisted()


@pytest.fixture(scope='function')
def builder():
    _builder = flatbuffers.Builder(0)
    return _builder


#
# ACTIVATION TOKEN
#


def fill_token(token):
    token.oid = uuid.uuid4()
    token.atype = 1
    token.status = 1
    token.created = datetime.utcnow()
    token.completed = None
    token.code = util.generate_activation_code()
    token.email = 'homer.simpson@example.com'
    token.pubkey = binascii.b2a_hex(os.urandom(32)).decode()


@pytest.fixture(scope='function')
def token_fbs():
    _token = ActivationTokenFbs()
    fill_token(_token)
    return _token


@pytest.fixture(scope='function')
def token_cbor():
    _token = ActivationToken()
    fill_token(_token)
    return _token


def test_token_fbs_roundtrip(token_fbs, builder):
    # serialize to bytes (flatbuffers) from python object
    obj = token_fbs.build(builder)
    builder.Finish(obj)
    data = builder.Output()
    assert len(data) == 224

    # create python object from bytes (flatbuffes)
    _token = ActivationTokenFbs.cast(data)

    # assert _token == token_fbs

    assert _token.oid == token_fbs.oid
    assert _token.atype == token_fbs.atype
    assert _token.status == token_fbs.status
    assert _token.completed == token_fbs.completed
    assert _token.code == token_fbs.code
    assert _token.email == token_fbs.email
    assert _token.pubkey == token_fbs.pubkey


def test_token_cbor_roundtrip(token_cbor):
    # serialize to bytes (cbor) from python object
    obj = token_cbor.marshal()
    data = cbor.dumps(obj)
    assert len(data) == 212

    # create python object from bytes (cbor)
    _obj = cbor.loads(data)
    _token = ActivationToken.parse(_obj)

    # assert _token == token_cbor

    assert _token.oid == token_cbor.oid
    assert _token.atype == token_cbor.atype
    assert _token.status == token_cbor.status
    assert _token.completed == token_cbor.completed
    assert _token.code == token_cbor.code
    assert _token.email == token_cbor.email
    assert _token.pubkey == token_cbor.pubkey


def test_token_copy_cbor_to_fbs(token_cbor):
    token_fbs = ActivationTokenFbs()
    token_fbs.copy(token_cbor)

    # assert token_fbs == token_cbor

    assert token_fbs.oid == token_cbor.oid
    assert token_fbs.atype == token_cbor.atype
    assert token_fbs.status == token_cbor.status
    assert token_fbs.completed == token_cbor.completed
    assert token_fbs.code == token_cbor.code
    assert token_fbs.email == token_cbor.email
    assert token_fbs.pubkey == token_cbor.pubkey


def test_token_copy_fbs_to_cbor(token_fbs):
    token_cbor = ActivationToken()
    token_cbor.copy(token_fbs)

    # assert token_cbor == token_fbs

    assert token_cbor.oid == token_fbs.oid
    assert token_cbor.atype == token_fbs.atype
    assert token_cbor.status == token_fbs.status
    assert token_cbor.completed == token_fbs.completed
    assert token_cbor.code == token_fbs.code
    assert token_cbor.email == token_fbs.email
    assert token_cbor.pubkey == token_fbs.pubkey


#
# USER
#


def fill_user(user):
    user.oid = uuid.uuid4()

    user.label = 'Homer the 3rd'
    user.description = 'My motto as a user is: never read the f** manual;)'
    user.tags = ['geek', 'pythonista', 'lemon']

    user.email = 'homer.simpson@example.com'
    user.registered = datetime.utcnow()
    user.pubkey = binascii.b2a_hex(os.urandom(32)).decode()


@pytest.fixture(scope='function')
def user_fbs():
    _user = UserFbs()
    fill_user(_user)
    return _user


@pytest.fixture(scope='function')
def user_cbor():
    _user = User()
    fill_user(_user)
    return _user


def test_user_fbs_roundtrip(user_fbs, builder):
    # serialize to bytes (flatbuffers) from python object
    obj = user_fbs.build(builder)
    builder.Finish(obj)
    data = builder.Output()

    # create python object from bytes (flatbuffes)
    _user = UserFbs.cast(data)

    # assert _user == user_fbs

    assert _user.oid == user_fbs.oid
    assert _user.label == user_fbs.label
    assert _user.description == user_fbs.description
    assert _user.tags == user_fbs.tags
    assert _user.email == user_fbs.email
    assert _user.registered == user_fbs.registered
    assert _user.pubkey == user_fbs.pubkey


def test_user_cbor_roundtrip(user_cbor):
    # serialize to bytes (cbor) from python object
    obj = user_cbor.marshal()
    data = cbor.dumps(obj)

    # create python object from bytes (cbor)
    _obj = cbor.loads(data)
    _user = User.parse(_obj)

    # assert _user == user_cbor

    assert _user.oid == user_cbor.oid
    assert _user.label == user_cbor.label
    assert _user.description == user_cbor.description
    assert _user.tags == user_cbor.tags
    assert _user.email == user_cbor.email
    assert _user.registered == user_cbor.registered
    assert _user.pubkey == user_cbor.pubkey


def test_user_copy_cbor_to_fbs(user_cbor):
    user_fbs = UserFbs()
    user_fbs.copy(user_cbor)

    # assert user_fbs == user_cbor

    assert user_fbs.oid == user_cbor.oid
    assert user_fbs.label == user_cbor.label
    assert user_fbs.description == user_cbor.description
    assert user_fbs.tags == user_cbor.tags
    assert user_fbs.email == user_cbor.email
    assert user_fbs.registered == user_cbor.registered
    assert user_fbs.pubkey == user_cbor.pubkey


def test_user_copy_fbs_to_cbor(user_fbs):
    user_cbor = User()
    user_cbor.copy(user_fbs)

    # assert user_fbs == user_cbor

    assert user_fbs.oid == user_cbor.oid
    assert user_fbs.label == user_cbor.label
    assert user_fbs.description == user_cbor.description
    assert user_fbs.tags == user_cbor.tags
    assert user_fbs.email == user_cbor.email
    assert user_fbs.registered == user_cbor.registered
    assert user_fbs.pubkey == user_cbor.pubkey


#
# ORGANIZATION
#


def fill_org(org):
    org.oid = uuid.uuid4()
    org.label = 'My Org 1'
    org.description = 'Personal organization, created from unit test.'
    org.tags = ['previews', 'smb']
    org.name = 'homer23'
    org.otype = 1
    org.registered = datetime.utcnow()


@pytest.fixture(scope='function')
def org_fbs():
    org = OrganizationFbs()
    fill_org(org)
    return org


@pytest.fixture(scope='function')
def org_cbor():
    org = Organization()
    fill_org(org)
    return org


def test_org_fbs_roundtrip(org_fbs, builder):
    # serialize to bytes (flatbuffers) from python object
    obj = org_fbs.build(builder)
    builder.Finish(obj)
    data = builder.Output()
    assert len(data) == 192

    # create python object from bytes (flatbuffes)
    _org = OrganizationFbs.cast(data)

    # assert _org == org_fbs

    assert _org.oid == org_fbs.oid
    assert _org.label == org_fbs.label
    assert _org.description == org_fbs.description
    assert _org.tags == org_fbs.tags
    assert _org.name == org_fbs.name
    assert _org.otype == org_fbs.otype
    assert _org.registered == org_fbs.registered


def test_org_copy_fbs_to_cbor(org_fbs):
    org_cbor = Organization()
    org_cbor.copy(org_fbs)

    # assert org_cbor == org_fbs

    assert org_cbor.oid == org_fbs.oid
    assert org_cbor.label == org_fbs.label
    assert org_cbor.description == org_fbs.description
    assert org_cbor.tags == org_fbs.tags
    assert org_cbor.name == org_fbs.name
    assert org_cbor.otype == org_fbs.otype
    assert org_cbor.registered == org_fbs.registered


def test_org_cbor_roundtrip(org_cbor):
    # serialize to bytes (cbor) from python object
    obj = org_cbor.marshal()
    data = cbor.dumps(obj)
    assert len(data) == 177

    # create python object from bytes (cbor)
    _obj = cbor.loads(data)
    _org = Organization.parse(_obj)

    # assert _org == org_cbor

    assert _org.oid == org_cbor.oid
    assert _org.label == org_cbor.label
    assert _org.description == org_cbor.description
    assert _org.tags == org_cbor.tags
    assert _org.name == org_cbor.name
    assert _org.otype == org_cbor.otype
    assert _org.registered == org_cbor.registered


def test_org_copy_cbor_to_fbs(org_cbor):

    org_fbs = OrganizationFbs()
    org_fbs.copy(org_cbor)

    # assert org_fbs == org_cbor

    assert org_fbs.oid == org_cbor.oid
    assert org_fbs.label == org_cbor.label
    assert org_fbs.description == org_cbor.description
    assert org_fbs.tags == org_cbor.tags
    assert org_fbs.name == org_cbor.name
    assert org_fbs.otype == org_cbor.otype
    assert org_fbs.registered == org_cbor.registered
