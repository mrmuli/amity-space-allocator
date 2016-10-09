from amity import Amity
from room import Room

from collections import defaultdict
from random import randint

import os
import pickle
import random


class Person(Amity):
        """ Person subclasses Amity and is super to Fellow and Staff
                Person defines the main attributes and methods common
                to both Fellow and Class
         """
        total_people = {}
        staff = []

        def __init__(self):
            super(Amity, self).__init__()
            self.fellows = []
            self.allocated_people = []
            self.unallocated_people = []
            self.allocated_office = None
            self.allocated_livingspace = None

        def add_person(self, first_name, last_name, job_type, wants_accomodation):
            """
            Adds a person to the system and allocates a random room
            """
            self.first_name = first_name
            self.last_name = last_name
            self.job_type = job_type
            self.wants_accomodation = wants_accomodation

            self.username = first_name + last_name
            # add new person to the total people list with a new ID

            total_ids = len(Person.total_people)
            new_person_id = total_ids + 1
            self.person_id = new_person_id

            Person.total_people[new_person_id] = self.username

            # check the person's job type
            if job_type == 'Fellow':
                self.fellows.append(self.username)

                # sanity check for empty list errors
                if len(Room.offices) > 0:
                    # allocate an office to the new fellow
                    allocated_office = random.choice(Room.offices)
                    # allocate the new person as an occupant of selected room
                    # Room.total_rooms = defaultdict(list)
                    for key in Room.total_rooms.keys():

                        if key == allocated_office:
                            if len(Room.total_rooms[key]) == 6:
                                return "The office is currently fully occupied"
                            else:
                                Room.total_rooms[key].append(self.person_id)
                                print Room.total_rooms[key]

                else:
                    return "There are currently no offices"


                if wants_accomodation == 'Y':
                    # sanity check for empty list
                    if len(Room.livingspaces) > 1:
                        # allocate a random livingspace
                        allocated_livingspace = random.choice(Room.livingspaces)

                        # allocate the new person as an occupant of the livingspace
                        Room.total_rooms = defaultdict(list)
                        for key in Room.total_rooms.keys():
                            if key == allocated_livingspace:
                                if len(Room.total_rooms[key]) == 4:
                                    return "The livingspace is curently fully occupied"
                                else:
                                    Room.total_rooms[key].append(self.person_id)

                    else:
                        return "There are currently no livingspaces"

                elif wants_accomodation == 'N':
                    self.unallocated_people.append(self.username)


            elif job_type == 'Staff':

                Person.staff.append(self.username)
                allocated_office = random.choice(Room.offices)

                Room.total_rooms = defaultdict(list)
                for key, occupant in Room.total_rooms:
                    if key == allocated_office:
                        Room.total_rooms[key].append(self.person_id)

                if wants_accomodation == 'Y':
                    return "Staff members are not allocated livingspaces"

        def print_unallocated(self, filename, *args):
            """
            prints out unallocated people to a specified file
            """
            # if file output option specified in arguments, write to file
            if '-o' in args:
                with open(unallocated, 'wb') as f:
                    pickle.dump(self.unallocated_people, f)
            # if file output option not specified, write to screen(console)
            else:
                for person in self.unallocated_people:
                    print person

        def reallocate_person(self, person_id, room_name):
            """
            Reallocates a person to a new room
            """
            # check for the person's existance
            if person_id not in Person.total_people.keys():
                return "The person ID does not exist!"

            # check for the room's existance
            if room_name not in Room.total_rooms.keys():
                return "The room either desn't exist or is not allocated!"

            # check whether the person is already in the allocated room
            for room in Room.total_rooms.iteritems():
                if room == room_name:
                    for occupant in Room.total_rooms[room_name]:
                        if person_id == occupant:
                            return "The Person is already allocated in the requested room"

            # remove person in the already allocated room
            for room in Room.total_rooms.keys():
                for occupant in Room.total_rooms[room]:
                    if person_id == occupant:
                        Room.total_rooms[room].remove(person_id)

            # start office allocation, if room is an office
            if room_name in Room.offices:

                for key in Room.total_rooms.keys():
                    if key == room_name:
                        if len(Room.total_rooms[key]) == 6:
                            return "Sorry the office is occupied fully"
                        else:
                            Room.total_rooms[key].append(person_id)
                            print "Allocation to New office successfull!"

            # start livingspace allocation if room is a livingspace
            elif room_name in Room.livingspaces:

                for key in Room.total_rooms.iteritems():
                    if key == room_name:
                        if len(Room.total_rooms[key]) == 4:
                            return "Sorry the LivingSpace is currently fully occupied!"
                        else:
                            Room.total_rooms[key].append(person_id)
                            print "Allocation to New livingSpace successful!"


        def load_people(self, filename):
            """
            Adds people to rooms from a text file
            """
            pass
