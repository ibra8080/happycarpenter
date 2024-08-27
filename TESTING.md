# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

## Code Validation

### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| Directory | File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| authentication | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/authentication/serializers.py) | ![screenshot](documentation/validation/p1.png) | |
| authentication | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/authentication/urls.py) | ![screenshot](documentation/validation/p2.png) | |
| authentication | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/authentication/views.py) | ![screenshot](documentation/validation/p3.png) | |
| follows | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/follows/models.py) | ![screenshot](documentation/validation/p4.png) | |
| follows | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/follows/serializers.py) | ![screenshot](documentation/validation/p5.png) | |
| follows | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/follows/views.py) | ![screenshot](documentation/validation/p6.png) | |
| happy_carpenter_api | authentication.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/happy_carpenter_api/authentication.py) | ![screenshot](documentation/validation/p7.png) | |
| happy_carpenter_api | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/happy_carpenter_api/serializers.py) | ![screenshot](documentation/validation/p8.png) | |
| happy_carpenter_api | settings.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/happy_carpenter_api/settings.py) | ![screenshot](documentation/validation/p9.png) | |
| happy_carpenter_api | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/happy_carpenter_api/urls.py) | ![screenshot](documentation/validation/p10.png) | |
| happy_carpenter_api | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/happy_carpenter_api/views.py) | ![screenshot](documentation/validation/p11.png) | |
| likes | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/likes/models.py) | ![screenshot](documentation/validation/p12.png) | |
| likes | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/likes/serializers.py) | ![screenshot](documentation/validation/p13.png) | |
| likes | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/likes/views.py) | ![screenshot](documentation/validation/p14.png) | |
| posts | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/posts/models.py) | ![screenshot](documentation/validation/p15.png) | |
| posts | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/posts/serializers.py) | ![screenshot](documentation/validation/p16.png) | |
| posts | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/posts/views.py) | ![screenshot](documentation/validation/p17.png) | |
| professionals | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/professionals/models.py) | ![screenshot](documentation/validation/p18.png) | |
| professionals | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/professionals/serializers.py) | ![screenshot](documentation/validation/p19.png) | |
| professionals | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/professionals/views.py) | ![screenshot](documentation/validation/p20.png) | |
| profiles | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/profiles/models.py) | ![screenshot](documentation/validation/p21.png) | |
| profiles | serializers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/profiles/serializers.py) | ![screenshot](documentation/validation/p22.png) | |
| profiles | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/ibra8080/happycarpenter/main/profiles/views.py) | ![screenshot](documentation/validation/p23.png) | |

## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:
## Defensive Programming

| Endpoint | User Action | Expected Result | Pass/Fail | Comments |
| --- | --- | --- | --- | --- |
| User Registration | | | | |
| | Submit registration with missing required fields | API returns 400 Bad Request | Pass | Clear error message provided |
| | Submit registration with invalid email format | API returns 400 Bad Request | Pass | Email validation error returned |
| | Submit registration with password too short | API returns 400 Bad Request | Pass | Password length requirement enforced |
| | Submit registration with valid data | API returns 201 Created | Pass | New user created successfully |
| Authentication | | | | |
| | Login with incorrect credentials | API returns 401 Unauthorized | Pass | Generic error message to prevent user enumeration |
| | Access protected endpoint without token | API returns 401 Unauthorized | Pass | |
| | Access protected endpoint with expired token | API returns 401 Unauthorized | Pass | Clear message about token expiration |
| | Access protected endpoint with valid token | API allows access | Pass | |
| Posts | | | | |
| | Create post without authentication | API returns 401 Unauthorized | Pass | |
| | Create post with valid data | API returns 201 Created | Pass | New post created successfully |
| | Update another user's post | API returns 403 Forbidden | Pass | Users can only update their own posts |
| | Delete another user's post | API returns 403 Forbidden | Pass | Users can only delete their own posts |
| Comments | | | | |
| | Post comment without authentication | API returns 401 Unauthorized | Pass | |
| | Post valid comment | API returns 201 Created | Pass | Comment added successfully |
| Likes | | | | |
| | Like a post without authentication | API returns 401 Unauthorized | Pass | |
| | Unlike a post | API removes like | Pass | 204 No Content on successful unlike |
| Search and Filter | | | | |
| | Search with SQL injection attempt | API sanitizes input | Pass | Prevents SQL injection attacks |
| | Filter with invalid parameters | API ignores invalid params | Pass | Returns results based on valid params only |
| Error Handling | | | | |
| | Trigger a 500 Internal Server Error | API returns generic error message | Pass | Logs detailed error, returns safe message to client |
| Data Validation | | | | |
| | Submit data with incorrect types | API returns 400 Bad Request | Pass | Clear error messages about expected types |
| | Submit data exceeding max length | API returns 400 Bad Request | Pass | Enforces max length for relevant fields |

## Bugs

- ValueError at /posts/: Must supply cloud_name in tag or in configuration

    ![screenshot](documentation/bugs/cloudinary_config_error.png)

    - To fix this, I needed to properly configure the Cloudinary settings in my Django project. This involved:
      1. Ensuring that the `CLOUDINARY_STORAGE` dictionary in `settings.py` included the `cloud_name` key.
      2. Verifying that the `CLOUDINARY_URL` environment variable was correctly set with the full Cloudinary URL, including the cloud name.
      3. Double-checking that the Cloudinary Python SDK was properly installed and up-to-date.
      4. Restarting the Django development server after making these changes.

    After implementing these steps, the Cloudinary integration worked correctly, and I was able to handle image uploads and retrievals for posts without issues.

- IntegrityError at /reviews/: null value in column "professional_id" of relation "professionals_review" violates not-null constraint

    ![screenshot](documentation/bugs/review_integrity_error.png)

    - To fix this, I needed to address the issue with the `professional_id` field in the Review model:
      1. I checked the Review model to ensure that the `professional` field was properly defined with `on_delete=models.CASCADE` and `null=False`.
      2. I reviewed the view handling the review creation to make sure it was correctly assigning the professional to the review before saving.
      3. I added validation in the serializer to ensure that a valid professional_id is provided when creating a review.
      4. I updated the frontend form to ensure it always sends a valid professional_id when submitting a review.
      5. I added a try-except block in the view to handle potential IntegrityErrors and return a meaningful error message to the user.

    After implementing these changes, the review creation process worked correctly, ensuring that every review was associated with a valid professional user.

-  RelatedObjectDoesNotExist at /api-auth/login/: User has no profile.

    ![screenshot](documentation/bugs/login_no_profile_error.png)

    - To fix this, I needed to address the issue of users not having associated profiles:
      1. I reviewed the user registration process to ensure that a profile is created automatically when a new user signs up.
      2. I added a post_save signal for the User model to create a profile if it doesn't exist:

        ```python
        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)
        ```

      3. I ran a management command to create profiles for any existing users without them:

        ```python
        from django.core.management.base import BaseCommand
        from django.contrib.auth.models import User
        from profiles.models import Profile

        class Command(BaseCommand):
            help = 'Creates user profiles for users without one'

            def handle(self, *args, **options):
                users_without_profile = User.objects.filter(profile__isnull=True)
                for user in users_without_profile:
                    Profile.objects.create(user=user)
                    self.stdout.write(f'Created profile for user {user.username}')
        ```

      4. I updated the login view to handle cases where a user might not have a profile, creating one if necessary.

    After implementing these changes, the login process worked correctly for all users, ensuring that every user has an associated profile.

- DisallowedHost at /: Invalid HTTP_HOST header

    ![screenshot](documentation/bugs/disallowed_host_error.png)

    - To fix this, I added the development server's hostname to the ALLOWED_HOSTS setting in settings.py:
      ```python
      ALLOWED_HOSTS = ['8000-ibra8080-happycarpenter-yehn5hgpju1.ws.codeinstitute-ide.net', 'localhost', '127.0.0.1']
      ```
    This allows Django to accept requests from the development server, resolving the DisallowedHost error.

- KeyError at /profiles/: 'request'

    ![screenshot](documentation/bugs/profiles_key_error.png)

    - To fix this, I needed to update the `get_is_owner` method in the ProfileSerializer:
      ```python
      def get_is_owner(self, obj):
          request = self.context.get('request')
          return request.user == obj.owner if request and request.user.is_authenticated else False
      ```
    This ensures that the method can handle cases where the request might not be available in the serializer's context.

- IntegrityError at /auth/register/: duplicate key value violates unique constraint "profiles_profile_owner_id_key"

    ![screenshot](documentation/bugs/register_integrity_error.png)

    - To fix this, I needed to prevent the creation of duplicate profiles:
      1. I updated the user registration process to create a profile only if one doesn't already exist.
      2. I added a signal to create a profile when a new user is created:
        ```python
        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.get_or_create(owner=instance)
        ```
      3. I added a unique constraint to the Profile model to ensure each user can only have one profile:
        ```python
        class Profile(models.Model):
            owner = models.OneToOneField(User, on_delete=models.CASCADE)
            # ... other fields ...
        ```
    These changes ensure that each user has exactly one profile, preventing the IntegrityError during registration.



## Unfixed Bugs

> [!NOTE]  
> There are no remaining bugs that I am aware of.
