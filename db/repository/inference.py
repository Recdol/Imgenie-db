from mongoengine import QuerySet
from ..document import (
    InferenceDocument,
    InferenceQueryEmbeddedDocument,
    InferenceOutputEmbeddedDocument,
    InferenceFeedbackEmbeddedDocument,
)
from ..exception import NotFoundInferenceException, NotFoundUserException
from ..model import User, Playlist, Song, Inference
from .common import (
    find_user_doc_by_dto,
    find_song_doc_by_dto,
    find_song_docs_by_dto,
    find_playlist_docs_by_dto,
)


class InferenceRepository:
    def create_inference(
        self,
        user: User,
        query_image_url: str,
        query_genres: list[str],
        output_playlists: set[Playlist],
        output_songs: set[Song],
        feedback_like_songs: set[Song] = [],
    ) -> Inference:
        query = InferenceQueryEmbeddedDocument(
            image_url=query_image_url, genres=query_genres
        )
        output = InferenceOutputEmbeddedDocument(
            playlists=find_playlist_docs_by_dto(output_playlists),
            songs=find_song_docs_by_dto(output_songs),
        )
        feedback = InferenceFeedbackEmbeddedDocument(
            like_songs=find_song_docs_by_dto(feedback_like_songs)
        )
        inference = InferenceDocument(
            user=find_user_doc_by_dto(user),
            query=query,
            output=output,
            feedback=feedback,
        )

        saved: InferenceDocument = inference.save()
        return saved.to_dto()

    def find_by_id(self, id: str) -> Inference | None:
        inference: InferenceDocument = InferenceDocument.objects(id=id).first()

        if not inference:
            return None

        return inference.to_dto()

    def find_by_user(self, user: User) -> list[Inference]:
        user_doc = find_user_doc_by_dto(user)

        if not user_doc:
            raise NotFoundUserException(f"Can't find User document: user={user}")

        inferences: QuerySet[InferenceDocument] = InferenceDocument.objects(
            user=user_doc
        )
        return [inference.to_dto() for inference in inferences]

    def add_feedback_like_song_by_id(self, id: str, song: Song) -> None:
        inference_doc = self._find_doc_by_id(id)

        if not inference_doc:
            raise NotFoundInferenceException(f"Can't find Inference document: id={id}")

        song_doc = find_song_doc_by_dto(song)
        inference_doc.feedback.like_songs.append(song_doc)
        inference_doc.save()

    def delete_feedback_like_song(self, id: str, song: Song) -> None:
        inference_doc = self._find_doc_by_id(id)

        if not inference_doc:
            raise NotFoundInferenceException(f"Can't find Inference document: id={id}")

        song_doc = find_song_doc_by_dto(song)
        inference_doc.feedback.like_songs.remove(song_doc)
        inference_doc.save()

    @classmethod
    def _find_doc_by_id(self, id: str) -> InferenceDocument:
        return InferenceDocument.objects(id=id).first()
