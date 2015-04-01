import requests
import json

"""
Provides a python interface to the MotorsportReg.com API using the requests library. This module only supports json.
See https://api.motorsportreg.com for authorization to use the API and details describing it.
pr_* prefixed functions are private API calls that require an MSR account that is affiliated and has been blessed by the organization.

TODO: update public_calendar function to include optional arguments
TODO: update pr_calendar function to include optional arguments
TODO: update pr_calendar_by_type function to include optional arguments
TODO: update pr_get_logbook_entry to support PUT and DELETE (currently only GET)

Software License:
MIT License (MIT)

Copyright (c) 2015. GeomaticsResearch LLC, Michael Ewald

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Author:
Michael Ewald (mewald@geomaticsresearch.com)
GeomaticsResearch LLC
http://GeomaticsResearch.com
"""

class MSRAPi(object):
    def __init__(self, organization_id, username, password):
        """
        https://api.motorsportreg.com
        """
        self.organization_id = organization_id
        self.username = username
        self.password = password
        self.url_prefix = "https://api.motorsportreg.com/rest/"

    def _public_request(self, rest_resource):
        """Get a response from an unauthenticated public REST resource"""
        r = requests.get(rest_resource)
        r.encoding = "utf-8"
        return r.json()

    def _authenticated_request(self, rest_resource):
        """
        Setup authentication and pass the X-Organization-Id header to allow us to use the authenticated sections of the API
        """
        r = requests.get(rest_resource, auth=requests.auth.HTTPBasicAuth(self.username, self.password), headers={'X-Organization-Id': self.organization_id})
        r.encoding = "utf-8"

        return r.json()

    def public_calendar(self, organization_id):
        """
        GET /rest/calendars/organization/{organization_id}
        Return a calendar of events for a single organization/club
        Optionally append ?archive=true to include events in the past
        """
        resource = "{0}calendars/organization/{1}.json".format(self.url_prefix, organization_id)
        response = self._public_request(resource)
        return response

    def pr_calendar(self):
        """
        GET /rest/calendars
        All events from all calendars starting today or later.
        Supports geospatial filtering by passing URL parameter "postalcode" with a five-digit American Zip Code or six-character Canadian Postal Code. Optionally specify "radius" which defaults to 300 miles. Optionally specify "start" and "end" to limit date range with ISO8601 dates like yyyy-mm-dd.
        """
        resource = "{0}calendars.json".format(self.url_prefix)
        response = self._authenticated_request(resource)
        return response

    def pr_venue_calendar(self, venue_id):
        """
        GET /rest/calendars/venue/{venue_id}
        Return a calendar of events for a single venue (Laguna Seca, Road Atlanta, ...)
        """
        resource = "{0}calendars/venue/{1}.json".format(self.url_prefix, venue_id)
        response = self._authenticated_request(resource)
        return response

    def pr_calendar_by_type(self, type_id):
        """
        GET /rest/calendars/type/{type_id}
        Return a calendar of events for a single type of event (HPDE, Autocross, Rally, ...)
        Supports geospatial filtering by passing URL parameter "postalcode" with a five-digit American Zip Code or six-character Canadian Postal Code. Optionally specify "radius" which defaults to 300 miles.
        """
        resource = "{0}calendars/type/{1}.json".format(self.url_prefix, type_id)
        response = self._authenticated_request(resource)
        return response

    def pr_attendees(self, event_id, include_questions=True):
        """
        GET /rest/events/{event_id}/attendees
        Authenticated request returns a complete list of attendees including all statuses.
        Questions may be included in partial response by passing ?fields=questions in URL"""
        if include_questions is True:
            resource = "{0}events/{1}/attendees.json?fields=questions".format(self.url_prefix, event_id)
        else:
            resource = "{0}events/{1}/attendees.json".format(self.url_prefix, event_id)
        response = self._authenticated_request(resource)
        return response

    def pr_assignments(self, event_id, include_instructors=True, include_team=True):
        """
        GET /rest/events/{event_id}/assignments
        Authenticated request returns a complete list of assignments (aka entries) including all statuses. Provides internal links to profiles and vehicles to obtain more details about an assignment.
        Co-drivers/Teams may be included in partial response by passing ?fields=team in URL
        Instructors may be included in partial response by passing ?fields=instructors in URL
        """
        if include_instructors is True and include_team is True:
            resource = "{0}events/{1}/assignments.json?fields=instructors,team".format(self.url_prefix, event_id)
        elif include_instructors is True and include_team is False:
            resource = "{0}events/{1}/assignments.json?fields=instructors".format(self.url_prefix, event_id)
        elif include_instructors is False and include_team is True:
            resource = "{0}events/{1}/assignments.json?fields=team".format(self.url_prefix, event_id)
        else:
            resource = "{0}events/{1}/assignments.json".format(self.url_prefix, event_id)
        response = self._authenticated_request(resource)
        return response

    def pr_assignments_by_segment(self, event_id, segment_id, include_instructors=True, include_team=True):
        """
        GET /rest/events/{event_id}/segments/{segment_id}/assignments
        Return a list of assignments for a single segment of an event
        """
        if include_instructors is True and include_team is True:
            resource = "{0}events/{1}/segments/{2}/assignments.json?fields=instructors,team".format(self.url_prefix, event_id, segment_id)
        elif include_instructors is True and include_team is False:
            resource = "{0}events/{1}/segments/{2}/assignments.json?fields=instructors".format(self.url_prefix, event_id, segment_id)
        elif include_instructors is False and include_team is True:
            resource = "{0}events/{1}/segments/{2}/assignments.json?fields=team".format(self.url_prefix, event_id, segment_id)
        else:
            resource = "{0}events/{1}/segments/{2}/assignments.json".format(self.url_prefix, event_id, segment_id)
        response = self._authenticated_request(resource)
        return response

    def pr_event_segments(self, event_id):
        """
        GET /rest/events/{event_id}/segments
        Return a list of segments with number, class, modifier and group options
        """
        resource = "{0}events/{1}/segments.json".format(self.url_prefix, event_id)
        response = self._authenticated_request(resource)
        return response

    def pr_members(self):
        """
        GET /rest/members
        Return a list of all members
        """
        resource = "{0}members.json".format(self.url_prefix)
        response = self._authenticated_request(resource)
        return response

    def pr_member(self, member_id, include_questions=True, include_history=True):
        """
        GET /rest/members/{member_id}
        Return a single member
        Registration history may be included in partial response by passing ?fields=history in URL
        Member questions may be included in partial response by passing ?fields=questions in URL
        """
        if include_questions is True and include_history is True:
            resource = "{0}members/{1}.json?fields=questions,history".format(self.url_prefix, member_id)
        elif include_questions is True and include_history is False:
            resource = "{0}members/{1}.json?fields=questions".format(self.url_prefix, member_id)
        elif include_questions is False and include_history is True:
            resource = "{0}members/{1}.json?fields=history".format(self.url_prefix, member_id)
        else:
            resource = "{0}members/{1}.json".format(self.url_prefix, member_id)
        response = self._authenticated_request(resource)
        return response

    def pr_profile(self, profile_id):
        """
        GET /rest/profiles/{profile_id}
        Return a single profile and the corresponding member_id
        """
        resource = "{0}profiles/{1}.json".format(self.url_prefix, profile_id)
        response = self._authenticated_request(resource)
        return response

    def pr_member_vehicles(self, member_id):
        """
        GET /rest/members/{member_id}/vehicles
        Return a list of vehicles for a single profile
        """
        resource = "{0}members/{1}/vehicles.json".format(self.url_prefix, member_id)
        response = self._authenticated_request(resource)
        return response

    def pr_member_vehicle(self, member_id, vehicle_id):
        """
        GET /rest/members/{member_id}/vehicles/{vehicle_id}
        Return a single vehicle for a single profile
        """
        resource = "{0}members/{1}/vehicles/{2}.json".format(self.url_prefix, member_id, vehicle_id)
        response = self._authenticated_request(resource)
        return response

    def pr_member_logbook(self, member_id):
        """
        GET /rest/members/{member_id}/logbook
        Return a list of log book entries about a single profile
        """
        resource = "{0}members/{1}/logbook.json".format(self.url_prefix, member_id)
        response = self._authenticated_request(resource)
        return response

    def pr_logbook_types(self):
        """
        GET /rest/logbooks/types
        Return a list of log book entry types
        """
        resource = "{0}logbooks/types.json".format(self.url_prefix)
        response = self._authenticated_request(resource)
        return response

    def pr_get_logbook_entry(self, logbook_entry_id):
        """
        GET/PUT/DELETE /rest/logbooks/{logbook_entry_id}
        Return, update or delete a single log book entry
        """
        resource = "{0}logbooks/{1}.json".format(self.url_prefix, logbook_entry_id)
        response = self._authenticated_request(resource)
        return response

    def pr_post_logbook_entry(self, payload):
        """
        POST /rest/logbooks
        Create a log book entry
        """
        resource = "{0}logbooks.json".format(self.url_prefix)
        r = requests.post(resource, auth=requests.auth.HTTPBasicAuth(self.username, self.password), headers={'X-Organization-Id': self.organization_id, 'content-type': 'application/vnd.pukkasoft+json'}, data=json.dumps(payload))
        return r