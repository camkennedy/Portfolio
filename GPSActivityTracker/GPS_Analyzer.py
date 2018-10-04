## [Cameron Kennedy]
'''### Program Overview ###
This program will take one or multiple GPX files, and provide summary information on them that I’ve found
difficult to obtain from existing software, specifically, both steepness analysis of a single event, and
analysis comparing multiple events.

For those unfamiliar, a GPX file (GPS Exchange Format) is an XML file generated from GPS data – often from fitness
devices such as watches, phones, or dedicated devices (e.g., a cycling GPS) – when a person records a journey
(typically an athletic event such as running, cycling, or hiking).  Most devices either store their data natively
in GPX format, or can export to GPX.

Complexities of this program include classes calling other classes, the inherent imprecise nature of GPS data
(especially with altitude data) and thus writing the necessary smoothing / approximating functions, working with the
file system, and file sizes (GPX files I use are typically hundreds of kilobytes, which is fairly small but in
aggregate could be a bit slow).

Users are required to supply their own GPX files, though several are included for testing purposes in folders d1 and
d2 (located in the program's main folder).'
'''
from datetime import datetime, timedelta
import numpy as np
import os  #Used for file & directory access
import gpxpy  #GPX parser
#If the gpxpy package is missing, the Anaconda installation command is: conda install -c conda-forge gpxpy
from sklearn.cluster import DBSCAN  #Used for clustering similar events
from operator import itemgetter

print('Welcome to the GPS Summary & Steepness Calculator!')
print()
print('***** W200 Instructors/Graders: Note, several sample GPX files for testing are located in '
      + 'sub-folders d1 and d2. *****')
print()

class Menu:
    '''Main menu function. Prompts the user to load a file, a folder, analyze the loaded data, or exit the program.'''
    def __init__(self):
        self.choice = 0
        self.choice_errormsg = '  INPUT ERROR! Please enter a valid main menu choice: 1, 2, 3 or 4.'
        self.data_to_analyze = None
        self.display_menu()

    def display_menu(self):
        '''Prints the menu, prompts users for choice, displays currently loaded file(s), and handles errors.'''
        #Print menu
        while self.choice != 4:
            if str(self.data_to_analyze) == 'None':
                self.data_to_analyze = None
            print()
            print('MAIN MENU')
            print('Currently loaded file / folder: ' + str(self.data_to_analyze)) #Print loaded files, or None
            print('Please choose from the following options:')
            print('  1. Load Single GPX File.')
            print('  2. Load Multiple GPX Files.')
            print('  3. Analyze Data.')
            print('  4. Quit the program.')

            try:
                self.choice = int(input('  Enter your choice here: '))
            except:
                self.choice = 0  #Resets to 0. Actual error message handled in 'else' statement below

            if self.choice == 1:
                print('\n### Load Single GPX File selected. ###')
                self.load_single_file()
            elif self.choice == 2:
                print('\n### Load Multiple GPX Files selected. ###')
                self.load_multi_file()
            elif self.choice == 3:
                print('\n### Analyze Data selected. ###')
                Analyze_Data(self.data_to_analyze)
            elif self.choice == 4:
                print('Goodbye!')
            else:
                print(self.choice_errormsg)

    def load_single_file(self):
        '''Solicits then passes a filename string (valid or invalid) to the Single_Event class.'''
        print('Please enter a file name. Absolute or relative path names are accepted.')
        filename = str(input())
        self.data_to_analyze = Single_Event(filename)

    def load_multi_file(self):
        '''Solicits then passes a directory string (valid or invalid) to the Multi_Event class.
        Directories with only 1 GPX file are convered to a Single_Event class.
        '''
        #For all files in folder, call Multi_Event to add them to a list.
        print('Please enter a directory (i.e., folder) name. Absolute or relative path names are accepted.')
        dir_name = str(input())
        self.data_to_analyze = Multi_Event(dir_name)
        if len(self.data_to_analyze.gpx_file_list) == 0:  #Convert to Single_Event class if only one event in list.
            self.data_to_analyze = None
        elif len(self.data_to_analyze.gpx_file_list) == 1:  #Convert to Single_Event class if only one event in list.
            print('Only one GPX file found in this folder. Treating as single file (Single_Event class).')
            self.data_to_analyze = self.data_to_analyze.gpx_file_list[0]

class Single_Event:
    '''Takes a filename (and path, optionally) and 'returns' a parsed GPX file in its self.event attribute.'''
    def __init__(self, file_loc):
        self.file_loc = file_loc
        self.event = None
        self.load_file()  #Learned __init__ methods can't return things (other than None), so calling separate method

    def load_file(self):
        '''Loads a single file.'''

        try:
            if self.file_loc[-4:] != '.gpx':
                raise Exception()
            gpx_file = open(self.file_loc, 'r')  #r for read-only
            self.event = gpxpy.parse(gpx_file)  #This is where gpxpy does its magic of interpreting the gpx xml code.
            self.event.adjust_time(timedelta(hours=-7))  #Offsets event times 7 hours from GMT.
            #A future version could include local time of the event, but it doesn't appear to be stored in the GPX file.
            gpx_file.close()

        except:
            print('Invalid file. Please enter a valid GPX file.')
            self.file_loc = None
            return None

    def __str__(self):
        if self.file_loc is not None:
            return str('Single Event: File = ' + os.path.basename(self.file_loc))  #Print file, not full path.
        else:
            return 'None'

class Multi_Event:
    '''Takes a directory and 'returns' a list of multiple Single_Event objects.'''
    def __init__(self, dir_loc):
        self.dir_loc = dir_loc
        self.gpx_file_list = []
        self.load_dir()

    def load_dir(self):
        '''Checks to ensure a valid directory is passed in, and if so, loops through every file to include all
        .gpx files as Single_Event objects in a list. Also sorts the list by event time, in descending order.
        '''
        if os.path.isdir(self.dir_loc): #Check if valid folder
            i = 0
            for fn in os.listdir(self.dir_loc):  #Loop through items in folder
                if fn.endswith('.gpx'):  #If it's a GPX file ...
                    i += 1
                    #Makes list of Single_Event objects by calling the Single_Event class.
                    try:
                        self.gpx_file_list.append(Single_Event(os.path.abspath(self.dir_loc) + '\\' + fn))
                    except:
                        print('BOGUS GPX FILE!')
                        i -= 1
                        continue
                    if i % 10 == 0:  #Give status every 10 files.
                        print('{} files loaded so far!'.format(i))
            print('{} total files loaded!'.format(i))
            if len(self.gpx_file_list) == 0:
                print('No GPX files found in this folder. Please choose a different folder.')
                return None
            else:  #Learned nifty way to sort list by attribute of object in list!
                self.gpx_file_list.sort(key=lambda obj:obj.event.time, reverse=True)
                self.group_like_events()

        else:
            print('Invalid directory selected. Please enter a valid directory. Returning to Main Menu.')
            self.dir_loc = None
            return None

    def __str__(self):
        return str('Multi_Event loaded, folder: ' + self.dir_loc)

    def group_like_events(self):
        '''Clusters like events together.  Then prompts the user with a list of events from which to choose.
        Then reduces the Multi_Event list (self.gpx_file_list) to only the events in that group.
        '''
        print('\nGrouping Events ...')

        #Build array of start_lat, start_lon, end_lat, end_lon, dist
        data_to_cluster = []
        items_to_remove = []
        i = -1
        event_dist_scale = 100000  #Used to scale event distance when clustering.
        for SE in self.gpx_file_list:  #SE stands for an instance of the Single_Event class.
            distance = 0
            duration = 0
            i += 1
            try:  #These occasionally fail, so wrapping them in a try statement and eliminating event upon failure.
                distance = Conversions(SE.event.length_2d()).meters_to_miles()
                duration = SE.event.get_duration()
            except:
                items_to_remove.append(i)
                continue
            if distance < 0.25 or duration < (5 * 60):  #Exclude events < 0.25 miles or < 5 min.
                items_to_remove.append(i)
            else:
                data_to_cluster.append([SE.event.length_2d() / event_dist_scale,
                                            #Convert meters to smaller scale for clustering
                                        SE.event.get_points_data()[0].point.latitude,
                                        SE.event.get_points_data()[0].point.longitude,
                                        SE.event.get_points_data()[-1].point.latitude,
                                        SE.event.get_points_data()[-1].point.longitude,])
        print('Removing {} events because they were too short or failed to load.'.format(len(items_to_remove)))
        if items_to_remove != []:
            items_to_keep = set(range(len(self.gpx_file_list))) - set(items_to_remove)
            self.gpx_file_list = itemgetter(*items_to_keep)(self.gpx_file_list)

        if len(data_to_cluster) == 0:
            print('The selected directory does contains no valid gpx files. Nothing to analyze. Returning to Main Menu.')
            self.gpx_file_list = []
        else:
            db = DBSCAN(eps=0.005, min_samples=2).fit(np.array(data_to_cluster)) #Clustering algorithm
            '''This is where the clustering "magic" happens.  The eps variable took a fair amount of tweaking to
            get right, along with manually scaling the distance variable to be a similar (roughly) scale as the
            lat & lon variables.  This approach is admittedly not perfect, but it works.  Also, this clustering
            algorithm will fail near the North and South Poles due to converging longitudes; I can live with that.
            Set min_samples=2 to allow for groups as small as 2 events.
            '''

            labels = list(db.labels_)  #List of all events and their groups.
                #Makes a list of events from 0 to groups_count. -1 indicates an individual event (unique, not clusetered).
            indiv_events_count = labels.count(-1)
            total_events_count = len(labels)
            groups_count = max(labels) + 1
            print('You have {} total events. '.format(len(labels)))
            if groups_count == 0:
                print('None of them are the same event. Nothing to analyze. Returning to Main Menu.')
                self.gpx_file_list = []
            else:
                print('{} are unique events (not grouped), with the remaining '.format(indiv_events_count)
                      + '{} clustered into {} groups.'.format(total_events_count - indiv_events_count, groups_count)
                     )
                print('Here are the groups of events:')

                for i in range(groups_count):
                    distance = Conversions(data_to_cluster[labels.index(i)][0] * event_dist_scale).meters_to_miles()
                    print('  Event Group {}: {} events, {:.2f} mi., '.format(i+1, labels.count(i), distance)
                          + 'Most recent: {:%D %H:%M:%S}'.format(self.gpx_file_list[labels.index(i)].event.get_time_bounds()[0])
                         )

                input_text = ('Please enter the number of the group you would like to analyze.\n' +
                             'Enter 0 to return to the main menu.')
                print('\n' + input_text)
                #I considered an option to analyze all events, but the analysis becomes nonsensical, so I opted against it.

                #Whittle down list of events to only those in selected groups:
                x = None
                while x not in range(groups_count + 1):
                    try:
                        x = int(input())
                        if x == 0:
                            self.gpx_file_list = []
                        elif 1 <= x <= groups_count:
                            indicies = [index for index, value in enumerate(labels) if value == x-1]
                            #* lets itemgetter accept a list.
                            self.gpx_file_list = itemgetter(*indicies)(self.gpx_file_list)
                        else:
                            raise Exception()
                    except:
                        x = None
                        print('\nInvalid input. ' + input_text)

class Analyze_Data:
    '''Takes a Single_Event or Multi_Event object as input.  For Single_Event objects, it prints summary statistics
    including a steepness breakdown.  For Multi_Event objects, it prints summary statistics along with a listing
    of each event, including a comparison to the best and median times for that event.
    '''
    def __init__(self, obj_to_analyze):
        print('\nAnalyzing Data ...')

        self.obj_to_analyze = obj_to_analyze

        if isinstance(self.obj_to_analyze, Single_Event):
            self.analyze_single()
        elif isinstance(self.obj_to_analyze, Multi_Event):
            self.analyze_multi()
        else:
            print('No data found or wrong type of data loaded. Please reload data and try again.')

    def analyze_single(self):
        '''Analyze a Single_Event instance. Calculates summary stats and steepness bands.'''
        print('Analyzing Single Event.')
        event = self.obj_to_analyze.event

        #CALCULATE SUMMARY STATS.
        #Grab summary stats
        start_end_times = event.get_time_bounds()
        duration = event.get_duration()
        distance = Conversions(event.length_2d()).meters_to_miles()
        asc_des = event.tracks[0].get_uphill_downhill()
        asc = Conversions(asc_des[0]).meters_to_feet()
        des = Conversions(asc_des[1]).meters_to_feet()

        #Print summary stats
        print('Here\'s a summary of your event.')
        print('  Start Date & Time: {:%D %H:%M:%S}.'.format(start_end_times[0]))
        print('  End Date & Time: {:%D %H:%M:%S}.'.format(start_end_times[1]))
        print('  Duration: {:%H:%M:%S}.'.format(Conversions(duration).sec_to_datetime()))
        print('  Distance: {:.2f} miles.'.format(distance))
        print('  Average Speed: {:.1f} mph.'.format(distance / (duration/3600)))
        print('  Elevation Ascent / Descent: {:,.0f} ft. / {:,.0f} ft.'.format(asc, des))

        #CALCULATE STEEPNESS GRADES
        #Bucket into 10 groups, symmetrically distributed around 0.
        dists = []
        grades = []
        smooth_dist_thresh = 5  #Length in meters.
        '''Had to tweak this several times to get a good value for smoothing.'''

        #Grab points
        '''Makes a new list of points that are at least smooth_dist_thresh apart.'''
        prev_item = event.get_points_data()[0]
        for item in event.get_points_data():
            if item.point.distance_2d(prev_item.point) > smooth_dist_thresh:  #Serves as a smoothing function.
                distance = item.point.distance_2d(prev_item.point)
                dists.append(distance)

                #Calculate all grades
                ele_change = item.point.elevation - prev_item.point.elevation
                if distance > 0:
                    grades.append(ele_change / distance)
                else:
                    grades.append(0)
                prev_item = item

        #Also a smoothing component, to remove the most extreme grades (since they're typically erroneous).
        #Gets the indicies of the top and bottom grades, then removes those items from both grades and lists.
        pct_thresh = 5
        lower_pct = np.percentile(grades, pct_thresh)
        upper_pct = np.percentile(grades, 100 - pct_thresh)
        indices_to_omit = []
        i = 0
        for item in grades:
            if item > upper_pct or item < lower_pct:
                indices_to_omit.append(i)
            i += 1

        items_to_keep = set(range(len(grades))) - set(indices_to_omit)
        grades = itemgetter(*items_to_keep)(grades)
        dists = itemgetter(*items_to_keep)(dists)

        if len(dists) != len(grades):
            print('WARNING! Distance and Grade list lengths aren\'t the same.')

        #Get min/max grade; calculate upper grade boundary (5%, 10%, 15%, 20%, etc.; use absolute grade)
        max_abs_grade = abs(max(grades, key=abs))
        #Round to the nearest 0.05 higher than highest absolute grade
        max_grade_bound = (((max_abs_grade*100)//5)*5 + 5)/100
        grade_incr = max_grade_bound / 5

        #Make list of 10 lists.
        dists_by_grade = []
        [dists_by_grade.append([]) for dummy in range(10)]

        #Assign distances to buckets. Loop through grades; determine which index (0-9); apply index for dists
        i = 0
        for grade in grades:
            #Math to determine bucket; better than looping
            index = int(10 - 10*(grade+max_grade_bound)/(max_grade_bound*2))
            dists_by_grade[index].append(dists[i])
            i += 1

        dist_grades = sum(sum(i) if isinstance(i, list) else i for i in dists_by_grade) #Quickly sums 2-level list.
        '''Important to sum distance associated with grades and use that to calc %'s.
        It'll vary slightly vs. actual event distance. That's okay because we're getting the percentage of grades,
        so the variation in distances is negligible. But the %'s won't add up if using event distance.
        '''

        #Scales grade output back to actual distance travelled
        scale_factor = event.length_2d() / dist_grades

        print('  Steepness Breakdown:')
        for i in range(10):
            print('    {:+.0%} to {:+.0%} grade: '.format(max_grade_bound-grade_incr, max_grade_bound), end='')
            print('{:.2f} mi., '.format(Conversions(sum(dists_by_grade[i])).meters_to_miles()*scale_factor), end='')
            print('{:.0%} of distance.'.format(sum(dists_by_grade[i]) / dist_grades))
            max_grade_bound -= grade_incr

    def analyze_multi(self):
        '''Prints summary statistics and comparisons of multiple events in the selected group.'''
        print('Analyzing Multiple Events.')
        events = self.obj_to_analyze.gpx_file_list

        durations_list = []
        speeds_list = []

        for SE in events:  #SE stands for an instance of the Single_Event class
            durations_list.append(SE.event.get_duration())

        distance = Conversions(events[0].event.length_2d()).meters_to_miles()
        dur_min = min(durations_list)
        dur_med = np.median(durations_list)
        dur_max = max(durations_list)
        dur_fastest = Conversions(dur_min).sec_to_datetime()
        dur_median = Conversions(dur_med).sec_to_datetime()
        dur_slowest = Conversions(dur_max).sec_to_datetime()
        speed_fastest = distance / (dur_min/3600)
        speed_median = distance / (dur_med/3600)
        speed_slowest = distance / (dur_max/3600)

        print('Here\'s a summary of this event group!')
        print('  You have completed this event {} times.'.format(len(events)))
        print('  Distance: {:.2f} mi.'.format(distance))
        print('  Duration and Speed Summary: ')
        print('    Fastest: {:%H:%M:%S}, {:.1f} mph avg.'.format(dur_fastest, speed_fastest))
        print('    Median: {:%H:%M:%S}, {:.1f} mph avg.'.format(dur_median, speed_median))
        print('    Slowest: {:%H:%M:%S}, {:.1f} mph avg.'.format(dur_slowest, speed_slowest))
        print()
        print('  Specific events:')

        #Remember, list is already sorted from most recent to least recent
        i = 0
        for SE in events:  #SE stands for an instance of the Single_Event class
            i += 1
            dur_event = durations_list[i-1]
            dur_vs_median = ((dur_event / dur_med) - 1) * (-1)
            dur_vs_best = ((dur_event / dur_min) - 1) * (-1)
            print('    {}. Date/Time: {:%D %H:%M:%S}'.format(i, SE.event.time)
                  + ', Duration: {:%H:%M:%S}, '.format(Conversions(dur_event).sec_to_datetime())
                  + '{:+.1%} vs. Median, {:+.1%} vs. Fastest.'.format(dur_vs_median, dur_vs_best)
                 )

class Conversions:
    '''A handful of conversions used across different classes.'''
    def __init__(self, value_in):
        self.value_in = value_in

    def meters_to_miles(self):
        return self.value_in * 0.000621371

    def meters_to_feet(self):
        return self.value_in * 3.28084

    def sec_to_datetime(self):
        '''Converts an integer of seconds to a datetime object.'''
        return datetime(1,1,1) + timedelta(seconds=int(self.value_in))

Menu();  #Run it!
