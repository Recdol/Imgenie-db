from ..document import InferenceDocument, InferenceQueryEmbeddedDocument, InferenceOutputEmbeddedDocument, InferenceFeedbackEmbeddedDocument
from ..exception import NotFoundInferenceException
from ..model import User, Playlist, Song, Inference
from mongoengine import QuerySet


class InferenceRepository:
    def create_inference(
        self,
        user: User,
        query_image_url: str,
        query_genres: list[str],
        output_playlists: list[Playlist],
        output_songs: list[Song],
        feedback_like_songs: list[Song] = [],
    ) -> Inference:
        query = InferenceQueryEmbeddedDocument(image_url=query_image_url, genres=query_genres)
        output = InferenceOutputEmbeddedDocument(playlists=output_playlists, songs=output_songs)
        feedback = InferenceFeedbackEmbeddedDocument(like_songs=feedback_like_songs)
        inference = InferenceDocument(user=user, query=query, output=output, feedback=feedback)

        saved: InferenceDocument = inference.save()
        return saved.to_dto()

    def find_by_user(self, user: User) -> list[Inference]:
        inferences: QuerySet[InferenceDocument] = InferenceDocument.objects(user=user)
        return [inference.to_dto() for inference in inferences]

    def add_feedback_like_song_by_id(self, id: str, song: Song) -> None:
        inference_doc = self._find_doc_by_id(id)

        if not inference_doc:
            raise NotFoundInferenceException(f"Can't find Inference document: id={id}")

        inference_doc.feedback.like_songs.append(song)
        inference_doc.save()

    def delete_feedback_like_song(self, id: str, song: Song) -> None:
        inference_doc = self._find_doc_by_id(id)

        if not inference_doc:
            raise NotFoundInferenceException(f"Can't find Inference document: id={id}")

        inference_doc.feedback.like_songs.remove(song)
        inference_doc.save()

    @classmethod
    def _find_doc_by_id(self, id: str) -> InferenceDocument:
        return InferenceDocument.objects(id=id).first()
