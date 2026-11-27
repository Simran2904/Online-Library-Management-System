
USE library_db;

INSERT INTO books
(title, author, category_id, description, quantity, available_quantity, cover_image)
VALUES
(
    'The Alchemist',
    'Paulo Coelho',
    1,
    'A young shepherd travels in search of his personal legend.',
    5, 5, NULL
),
(
    'A Brief History of Time',
    'Stephen Hawking',
    2,
    'An introduction to the universe, space and time.',
    4, 4, NULL
),
(
    'Introduction to Algorithms',
    'Thomas H. Cormen',
    3,
    'A comprehensive guide to computer algorithms.',
    6, 6, NULL
),
(
    'Wings of Fire',
    'A. P. J. Abdul Kalam',
    5,
    'The autobiography of Dr. A. P. J. Abdul Kalam.',
    5, 5, NULL
),
(
    'The Discovery of India',
    'Jawaharlal Nehru',
    4,
    'A historical exploration of Indian culture and civilization.',
    3, 3, NULL
);
