# from sqlalchemy import (
#     Column,
#     Float,
#     ForeignKey,
#     Integer,
#     String,
#     create_engine,
#     func,
#     select,
# )
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# # ==============================
# # 1️⃣ Database Setup
# # ==============================

# engine = create_engine("sqlite:///playground.db", echo=True)
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()


# # ==============================
# # 2️⃣ Models
# # ==============================


# class Author(Base):
#     __tablename__ = "authors"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     country = Column(String)

#     books = relationship("Book", back_populates="author")

#     def __repr__(self):
#         return f"<Author(id={self.id}, name={self.name})>"


# class Publisher(Base):
#     __tablename__ = "publishers"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     city = Column(String)

#     books = relationship("Book", back_populates="publisher")

#     def __repr__(self):
#         return f"<Publisher(id={self.id}, name={self.name})>"


# class Book(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True)
#     title = Column(String, nullable=False)
#     price = Column(Float)

#     author_id = Column(Integer, ForeignKey("authors.id"))
#     publisher_id = Column(Integer, ForeignKey("publishers.id"))

#     author = relationship("Author", back_populates="books")
#     publisher = relationship("Publisher", back_populates="books")

#     def __repr__(self):
#         return f"<Book(id={self.id}, title={self.title}, price={self.price})>"


# # ==============================
# # 3️⃣ Create Tables
# # ==============================

# Base.metadata.create_all(bind=engine)


# # ==============================
# # 4️⃣ Session
# # ==============================

# db = SessionLocal()


# # ==============================
# # 5️⃣ Seed Data (only once)
# # ==============================

# # if not db.query(Author).first():
# #     a1 = Author(name="George Orwell", country="UK")
# #     a2 = Author(name="Haruki Murakami", country="Japan")

# #     p1 = Publisher(name="Penguin", city="London")
# #     p2 = Publisher(name="Vintage", city="New York")

# #     b1 = Book(title="1984", price=15.5, author=a1, publisher=p1)
# #     b2 = Book(title="Animal Farm", price=12.0, author=a1, publisher=p1)
# #     b3 = Book(title="Kafka on the Shore", price=18.0, author=a2, publisher=p2)

# #     db.add_all([a1, a2, p1, p2, b1, b2, b3])
# #     db.commit()


# def list_publishers(
#     db,
#     *,
#     limit: int = 10,
#     offset: int = 0,
#     sort_by: str = "id",  # id | name | book_count
#     order: str = "desc",  # asc | desc
#     city: str | None = None,
#     name_contains: str | None = None,
# ):
#     # -------------------------
#     # 1) Filters on publishers
#     # -------------------------
#     filters = []
#     if city is not None:
#         filters.append(Publisher.city == city)
#     if name_contains is not None:
#         # SQLite: LIKE is case-insensitive for ASCII by default (often), but don't rely on that.
#         # Keep it simple for playground:
#         filters.append(Publisher.name.like(f"%{name_contains}%"))

#     # -------------------------
#     # 2) TOTAL count query
#     #    Count publishers only (no join)
#     # -------------------------
#     count_base = select(Publisher.id)
#     if filters:
#         count_base = count_base.where(*filters)

#     total_stmt = select(func.count()).select_from(count_base.subquery())
#     total = db.execute(total_stmt).scalar_one()

#     # -------------------------
#     # 3) DATA query with book_count
#     # -------------------------
#     book_count = func.count(Book.id).label("book_count")

#     data_stmt = (
#         select(Publisher.id, Publisher.name, Publisher.city, book_count)
#         .select_from(Publisher)
#         .outerjoin(Book, Publisher.id == Book.publisher_id)
#     )
#     if filters:
#         data_stmt = data_stmt.where(*filters)

#     data_stmt = data_stmt.group_by(Publisher.id, Publisher.name, Publisher.city)

#     # -------------------------
#     # 4) Sorting allowlist (+ tie-breaker)
#     # -------------------------
#     ALLOWED_SORT = {
#         "id": Publisher.id,
#         "name": Publisher.name,
#         "city": Publisher.city,
#         "book_count": book_count,
#     }

#     sort_col = ALLOWED_SORT.get(sort_by)
#     if sort_col is None:
#         raise ValueError(f"Invalid sort_by={sort_by}. Allowed: {list(ALLOWED_SORT)}")

#     primary = sort_col.asc() if order == "asc" else sort_col.desc()

#     # deterministic order for pagination
#     data_stmt = data_stmt.order_by(primary, Publisher.id.desc())

#     # -------------------------
#     # 5) Pagination + execute
#     # -------------------------
#     data_stmt = data_stmt.limit(limit).offset(offset)
#     rows = db.execute(data_stmt).all()

#     return rows, total


# # ==============================
# # 6️⃣ 🧪 YOUR PRACTICE ZONE
# # ==============================

# print("\n--- All Books ---")

# # stmt = select(Book)
# # result = db.execute(stmt)
# # books = result.scalars().all()
# # print(books)

# # stmt = (
# #     select(Book)
# #     .where(Book.author_id == 2)
# #     .order_by(Book.title.desc(), Book.id.desc())
# #     .limit(5)
# #     .offset(1)
# # )
# # result = db.execute(stmt)
# # books = result.scalars().all()
# # print(books)

# # stmt = select(func.count()).where(Book.author_id == 2)
# # result = db.execute(stmt)
# # count = result.scalar_one()
# # print(count)

# # stmt = (select(Book.author_id, func.count())).group_by(Book.author_id)
# # result = db.execute(stmt)
# # print(result.all())

# # print(f"hello: {stmt.compile(compile_kwargs={'literal_binds': True})}")

# # stmt = select(Book.author_id).group_by(Book.author_id).having(func.count() > 3)
# # result = (db.execute(stmt)).scalars().all()
# # print(result)

# # print("\n
# # print("\n--- Books with price > 15 ---")
# # stmt = select(Book).where(Book.price > 15)
# # print(db.execute(stmt).scalars().all())

# # stmt = select(Book.title, Author.name).join(Author, Book.author_id == Author.id)
# # print(db.execute(stmt).scalars().all())


# # stmt = select(Book.title, Author.name).join(Author, Book.author_id == Author.id)
# # stmt = select(Book.title, Publisher.name).join(
# #     Publisher, Book.publisher_id == Publisher.id
# # )
# # stmt = (
# #     select(Book.title, Author.name, Publisher.name)
# #     .join(Author, Book.author_id == Author.id)
# #     .join(Publisher, Book.publisher_id == Publisher.id)
# # )
# # stmt = select(Author.name, Book.title).join(Book, Author.id == Book.author_id)
# # stmt = select(Author.name, Book.title).outerjoin(Book, Author.id == Book.author_id)
# # stmt = (
# #     select(Author.name, func.count(Book.id))
# #     .outerjoin(Book, Author.id == Book.author_id)
# #     .group_by(Author.name)
# # )
# # stmt = (
# #     select(Author.id, Author.name, func.count(Book.id).label("book_count"))
# #     .outerjoin(Book, Author.id == Book.author_id)
# #     .group_by(Author.id, Author.name)
# #     .order_by(func.count(Book.id).desc(), Author.id.desc())
# # )
# # stmt = (
# #     select(Publisher.id, Publisher.name, func.count(Book.id).label("book_count"))
# #     .outerjoin(Book, Publisher.id == Book.publisher_id)
# #     .group_by(Publisher.id, Publisher.name)
# #     .order_by(func.count(Book.id).desc(), Publisher.id.desc())
# # )
# def list_authors(
#     db,
#     *,
#     limit: int = 10,
#     offset: int = 0,
#     sort_by: str = "id",  # id | name | book_count
#     order: str = "desc",  # asc | desc
#     country: str | None = None,
#     name_contains: str | None = None,
# ):
#     # -------------------------
#     # 1) Filters on publishers
#     # -------------------------
#     filters = []
#     if country is not None:
#         filters.append(Author.country == country)
#     if name_contains is not None:
#         # SQLite: LIKE is case-insensitive for ASCII by default (often), but don't rely on that.
#         # Keep it simple for playground:
#         filters.append(Author.name.like(f"%{name_contains}%"))

#     # -------------------------
#     # 2) TOTAL count query
#     #    Count publishers only (no join)
#     # -------------------------
#     count_base = select(Author.id)
#     if filters:
#         count_base = count_base.where(*filters)
#     print(f"check query1: {count_base}")

#     total_stmt = select(func.count()).select_from(count_base.subquery())
#     total = db.execute(total_stmt).scalar_one()
#     print(f"my total: {total}")

#     # -------------------------
#     # 3) DATA query with book_count
#     # -------------------------
#     book_count = func.count(Book.id).label("book_count")

#     data_stmt = (
#         select(Author.id, Author.name, Author.country, book_count)
#         .select_from(Author)
#         .outerjoin(Book, Author.id == Book.author_id)
#     )
#     if filters:
#         data_stmt = data_stmt.where(*filters)

#     data_stmt = data_stmt.group_by(Author.id, Author.name, Author.country)

#     # -------------------------
#     # 4) Sorting allowlist (+ tie-breaker)
#     # -------------------------
#     ALLOWED_SORT = {
#         "id": Author.id,
#         "name": Author.name,
#         "country": Author.country,
#         "book_count": book_count,
#     }

#     sort_col = ALLOWED_SORT.get(sort_by)
#     if sort_col is None:
#         raise ValueError(f"Invalid sort_by={sort_by}. Allowed: {list(ALLOWED_SORT)}")

#     primary = sort_col.asc() if order == "asc" else sort_col.desc()

#     # deterministic order for pagination
#     data_stmt = data_stmt.order_by(primary, Author.id.desc())

#     # -------------------------
#     # 5) Pagination + execute
#     # -------------------------
#     data_stmt = data_stmt.limit(limit).offset(offset)
#     rows = db.execute(data_stmt).all()

#     return rows, total


# # rows, total = list_publishers(
# #     db,
# #     limit=10,
# #     offset=0,
# #     sort_by="book_count",
# #     order="desc",
# #     # city="London",
# #     # name_contains="Pen",
# # )
# rows, total = list_authors(
#     db,
#     limit=10,
#     offset=0,
#     sort_by="book_count",
#     order="desc",
# )
# print("TOTAL publishers:", total)
# print("ITEMS:")
# for r in rows:
#     print(r)

# stmt = select(Book.id, Author.name).limit(2).join(Author)
# result = db.execute(stmt)
# print(result.all())
# # stmt = (
# #     select(Book)
# #     .where(Book.author_id == 2, Book.title.like("%Book%"))
# #     .order_by(Book.id.desc())
# #     .limit(3)
# #     .offset(1)
# # )
# # print(db.execute(stmt).scalars().all())

# # print("\n--- Join Author + Book ---")
# # stmt = select(Book.title, Author.name).join(Book.author)
# # print(db.execute(stmt).all())


# # print("\n--- Count Books ---")
# # stmt = select(func.count(Book.id))
# # print(db.execute(stmt).scalar())


# db.close()
