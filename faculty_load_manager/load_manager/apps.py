from django.apps import AppConfig


def ss():
    from .models import Room
    try:
        x = Room.objects.get(room_name='310', room_category=1)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='310', room_category=1)
        x.save()
    try:
        x = Room.objects.get(room_name='311', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='311', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='312', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='312', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='313', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='313', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='314', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='314', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='315', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='315', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='300', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='300', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='302', room_category=1)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='302', room_category=1)
        x.save()
    try:
        x = Room.objects.get(room_name='316', room_category=1)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='316', room_category=1)
        x.save()


def startup():
    from .models import Year,SchoolYear,PreferredTime,DAY_OF_THE_WEEK
    from django.utils import timezone
    ss()
    # YEAR
    for i in range(1904,int(timezone.now().strftime("%Y")) +3):
        Year.objects.get_or_create(year=i)


    print("SCHOOL YEAR")
    try:
        current = SchoolYear.objects.get_or_create(
                                start_year= Year.objects.get(year = int(timezone.now().strftime("%Y"))) ,
                                end_year= Year.objects.get(year = int(timezone.now().strftime("%Y")) +1)
                                )
        print(int(timezone.now().strftime("%Y"))+2)
        next = SchoolYear.objects.get_or_create(
                                start_year= Year.objects.get(year = int(timezone.now().strftime("%Y"))+1) ,
                                end_year= Year.objects.get(year = int(timezone.now().strftime("%Y")) +2)
                                )

    except Exception as e:
        raise e

    try:
        if PreferredTime.objects.all().count() <= 0:
            for x,day in DAY_OF_THE_WEEK():
                for y, day in PreferredTime.TIME_SELECT:
                    try:
                        sched = PreferredTime.objects.get(
                        select_day = x,
                        select_time = y
                        )
                        print(f'{x} {y} already exists')
                    except PreferredTime.DoesNotExist:
                        sched = PreferredTime(
                            select_day = x,
                            select_time = y
                        )
                        sched.save()
            print("PREFERRED TIME INITIALIZED")
    except Exception as e:
        PreferredTime.objects.all().delete()
        raise e
class LoadManagerConfig(AppConfig):
    name = 'load_manager'

    def ready(request):
        print("READY")
        startup()
