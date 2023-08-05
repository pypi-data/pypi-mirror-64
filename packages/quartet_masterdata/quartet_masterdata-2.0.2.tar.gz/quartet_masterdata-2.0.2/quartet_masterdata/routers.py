# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.

from rest_framework.routers import DefaultRouter
from quartet_masterdata import viewsets

router = DefaultRouter()
router.register(
    r'locations',
    viewsets.LocationViewSet,
    basename='entries'
)
router.register(
    r'location-fields',
    viewsets.LocationFieldViewSet,
    basename='location-fields'
)
router.register(
    r'location-types',
    viewsets.LocationTypeViewSet,
    basename='location-types'
)
router.register(
    r'location-identifiers',
    viewsets.LocationIdentifierViewSet,
    basename='location-identifiers'
)
router.register(
    r'trade-items',
    viewsets.TradeItemViewSet,
    basename='trade-items'
)
router.register(
    r'companies',
    viewsets.CompanyViewSet,
    basename='companies'
)
router.register(
    r'company-types',
    viewsets.CompanyTypeViewSet,
    basename='company-types'
)
router.register(
    r'trade-item-fields',
    viewsets.TradeItemFieldViewSet,
    basename='trade-item-fields'
)
