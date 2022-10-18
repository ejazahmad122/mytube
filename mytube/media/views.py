from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Video, Comment, Like
from .serializers import CommentSerializer, LikeSerializer, VideoSerializer
from account.models import User

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class MediaView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """show all videos placed in data base 
        Args:
            request (Http): it will hold the data
        Returns:
            response (json): data about all videos
        """

        data = Video.objects.all()
        serializer = VideoSerializer(data, many=True)
        response = {
            'status_code': status.HTTP_200_OK,
            'status': "success",
            'data': serializer.data
        }
        return Response(response)

    def create(self, request):
        """store a video in related model mdoel:Video in data base

        Args:
            request (Http): hold the post request data

        Returns:
            response (json): data about the added video
        """
        try:
            loggedInUser = request.user
            user = User.objects.get(email=loggedInUser)
            request.data['user_id'] = user.id
            request.data['channel_name'] = user.channel_name
            serializer = VideoSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'status_code': status.HTTP_201_CREATED,
                    'status': "success",
                    'data': {"video": serializer.data}
                }
                return Response(response)
            return Response({"status": status.HTTP_400_BAD_REQUEST, 'message': "somthing went wrong while insertion !!"})
        except:
            return Response({"status": status.HTTP_400_BAD_REQUEST, 'message': "something went wrong while insertion !!"})


class CommentView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """show all comments placed in data base 
        Args:
            request (Http): it will hold the data
        Returns:
            response (json): data about all comments
        """
        try:
            data = Comment.objects.all()
            serializer = CommentSerializer(data, many=True)
            response = {
                'status_code': status.HTTP_200_OK,
                'status': "success",
                'data': serializer.data
            }
            return Response(response)
        except:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "something went wrong while listing videos !!"})

    def create(self, request):
        """store a comment of a videos in related model mdoel:Comment in data base

        Args:
            request (Http): hold the post request data

        Returns:
            response (json): data about the added comment
        """
        try:
            user = User.objects.get(email=request.user)
            request.data['user_id'] = user.id
            request.data['channel_name'] = user.channel_name
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'status_code': status.HTTP_201_CREATED,
                    'status': "success",
                    'data': {"comment": serializer.data}
                }
                return Response(response)
            return Response({"status": status.HTTP_400_BAD_REQUEST, 'message': "somthing went wrong while insertion !!"})
        except:
            return Response({"status": status.HTTP_400_BAD_REQUEST, 'message': "something went wrong while insertion !!"})

    def retrieve(self, request, pk=None):
        """show the comments of a specific video
        Args:
            pk (int): video id 
            request (Http): it will hold the data
        Returns:
            response (json): comments of the video
        """
        try:
            comments = []
            data = Comment.objects.filter(video_id=pk)
            for obj in data:
                user = User.objects.get(email=obj.user_id)
                comments.append(
                    {'user': user.channel_name, 'snippet': obj.snippet})
            response = {
                "status_code": status.HTTP_200_OK,
                "status": "success",
                "data": comments
            }
            return Response(response)
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': "something went wrong while retrieval !!"})


class LikeView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """show all likes placed in data base 
        Args:
            request (Http): it will hold the data
        Returns:
            response (json): data about all videos likes
        """
        try:
            data = Like.objects.all()

            serializer = LikeSerializer(data, many=True)
            response = {
                'status_code': 200,
                'status': "success",
                'data': serializer.data
            }
            return Response(response)
        except:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "something went wrong while listing likes !!"})

    def create(self, request):
        """store a like of a videos in related model mdoel:Like in data base

        Args:
            request (Http): hold the post request data

        Returns:
            response (json): data about the added Like of a video
        """
        try:
            option = request.data['option']
            user = User.objects.get(email=request.user)
            video_id = request.data['video_id']
            if option == 'like':
                video = Video.objects.get(id=video_id)
                Like.objects.create(user_id=user, video_id=video)
            else:
                Like.objects.filter(
                    user_id=user.id, video_id=video_id).delete()
            return Response({"status": status.HTTP_201_CREATED, 'message': "like updated !!"})
        except:
            return Response({"status": status.HTTP_400_BAD_REQUEST, 'message': "something went wrong while updation like !!"})

    def retrieve(self, request, pk=None):
        """show the likes of a specific video
        Args:
            pk (int): video id 
            request (Http): it will hold the data
        Returns:
            response (json): likes of the specific video
        """
        try:
            likes = []
            data = Like.objects.filter(video_id=pk)

            for obj in data:
                likes.append({'video_id': obj.video_id.id,
                             'user_id': obj.user_id.id})
            response = {
                "status_code": 200,
                "status": "success",
                "data": likes
            }
            return Response(response)
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': "something went wrong while retrieval !!"})
