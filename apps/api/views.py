# django packages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
# django rest framework packages
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as ObtainAuthTokenDRF
from rest_framework.response import Response
from rest_framework.views import APIView
# local packages
from apps.adopcion.models import Persona
from apps.mascota.models import Vacuna, Mascota
from apps.adopcion.serializers import PersonaSerializer
from apps.mascota.serializers import VacunaSerializer, MascotaSerializer, EditMascotaSerializer


def home(request):
    access_token = None
    if request.method == 'POST':
        token_instance, _ = Token.objects.get_or_create(user=request.user)
        access_token = token_instance.key

    return render(request, 'index.html', {
        'user_access_token': access_token,
    })


# region Persona views
class PersonaList(APIView):
    def get(self, request):
        queryset = Persona.objects.all()
        search_query = request.query_params.get('q')
        if search_query:
            args = [Q(nombre__contains=search_query) | Q(apellidos__contains=search_query) |
                    Q(email__contains=search_query)]
            queryset = queryset.filter(*args)
        serializer = PersonaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PersonaDetail(APIView):
    def get_object(self, pk):
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = PersonaSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = PersonaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region Vacuna views
class VacunaList(APIView):
    def get(self, request):
        queryset = Vacuna.objects.all()
        search_query = request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(nombre__contains=search_query)
        serializer = VacunaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VacunaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VacunaDetail(APIView):
    def get_object(self, pk):
        try:
            return Vacuna.objects.get(pk=pk)
        except Vacuna.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = VacunaSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = VacunaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region Mascota views
class MascotaList(APIView):
    def get(self, request):
        queryset = Mascota.objects.prefetch_related('persona').all()
        search_query = request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(
                nombre__contains=search_query,
                persona__nombre__contains=search_query,
                persona__apellidos__contains=search_query,
            )
        serializer = MascotaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EditMascotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MascotaDetail(APIView):
    def get_object(self, pk):
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = MascotaSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = EditMascotaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


class ObtainAuthToken(ObtainAuthTokenDRF):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'access_token': token.key,
            'token_type': 'Token',
        })


class VerifyAuthToken(APIView):
    def get(self):
        return Response()
