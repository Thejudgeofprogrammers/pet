import logging
from src.bd.database import Video, Article, Request_user, db
from src.app_module.dto.index import VideoDTO, ArticleDTO, RequestUserDTO
from sqlalchemy.exc import SQLAlchemyError


class Services:
    @staticmethod
    def submit(name: str, surname: str, phone: str, email: str, date) -> None:
        try:
            request_user = Request_user(name=name, surname=surname, phone=phone, email=email, date=date)
            
            if not all([name, surname, phone, email, date]):
                raise ValueError("Все поля должны быть заполнены")

            db.session.add(request_user)
            db.session.commit()
            
        except ValueError as ve:
            logging.error(f"Ошибка валидации: {ve}")

        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Ошибка при добавлении пользователя: {e}")

        finally:
            db.session.close()

    @staticmethod
    def add_video(title, description, video_url) -> None:
        try:
            new_video = Video(title=title, description=description, video_url=video_url)

            if not all([title, description, video_url]):
                raise ValueError("Все поля должны быть заполнены")

            db.session.add(new_video)
            db.session.commit()
  
        except ValueError as ve:
            logging.error(f"Ошибка валидации: {ve}")
    
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Ошибка при добавлении видео: {e}")

        finally:
            db.session.close()
    
    @staticmethod
    def add_article(title, description) -> None:
        try:
            new_article = Article(title=title, description=description)
            
            if not all([title, description]):
                raise ValueError("Все поля должны быть заполнены")

            db.session.add(new_article)
            db.session.commit()
            
        except ValueError as ve:
            logging.error(f"Ошибка валидации: {ve}")    

        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Ошибка при добавлении артикула: {e}")

        finally:
            db.session.close()
    
    @staticmethod
    def videos_list() -> list[VideoDTO]:
        videos = Video.query.order_by(Video.date_uploaded.desc()).all()
        return [VideoDTO(**video.__dict__) for video in videos]
    
    @staticmethod
    def articles_list() -> list[ArticleDTO]:
        articles = Article.query.order_by(Article.date_uploaded.desc()).all()
        return [Article(**article.__dict__) for article in articles]

    @staticmethod
    def view_notes() -> list[RequestUserDTO]:
        requests = Request_user.query.order_by(Request_user.date).all()
        return [Article(**request.__dict__) for request in requests]