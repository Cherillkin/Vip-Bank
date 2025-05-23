PGDMP  .                    }            vip_bank     15.12 (Debian 15.12-1.pgdg120+1)    17.0 y    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16605    vip_bank    DATABASE     s   CREATE DATABASE vip_bank WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE vip_bank;
                     postgres    false            �            1259    24792    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    16779 %   банковская_операция    TABLE     �   CREATE TABLE public."банковская_операция" (
    "id_банковской_операции" integer NOT NULL,
    "id_счета" integer,
    "сумма" integer,
    "id_операции" integer
);
 ;   DROP TABLE public."банковская_операция";
       public         heap r       postgres    false            �            1259    16778 >   банковская_опер_id_банковской_оп_seq    SEQUENCE     �   CREATE SEQUENCE public."банковская_опер_id_банковской_оп_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 W   DROP SEQUENCE public."банковская_опер_id_банковской_оп_seq";
       public               postgres    false    237            �           0    0 >   банковская_опер_id_банковской_оп_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."банковская_опер_id_банковской_оп_seq" OWNED BY public."банковская_операция"."id_банковской_операции";
          public               postgres    false    236            �            1259    16717    вид_счета    TABLE     �   CREATE TABLE public."вид_счета" (
    "id_вида_счета" integer NOT NULL,
    "название_вида_счета" character varying,
    "id_типа_счета" integer
);
 '   DROP TABLE public."вид_счета";
       public         heap r       postgres    false            �            1259    16716 ,   вид_счета_id_вида_счета_seq    SEQUENCE     �   CREATE SEQUENCE public."вид_счета_id_вида_счета_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 E   DROP SEQUENCE public."вид_счета_id_вида_счета_seq";
       public               postgres    false    229            �           0    0 ,   вид_счета_id_вида_счета_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."вид_счета_id_вида_счета_seq" OWNED BY public."вид_счета"."id_вида_счета";
          public               postgres    false    228            �            1259    16796 !   детали_инвестиций    TABLE       CREATE TABLE public."детали_инвестиций" (
    "id_детали" integer NOT NULL,
    "id_портфеля" integer,
    "id_типа_инвестиций" integer,
    "сумма" integer,
    "дата_покупки" timestamp without time zone
);
 7   DROP TABLE public."детали_инвестиций";
       public         heap r       postgres    false            �            1259    16795 5   детали_инвестиций_id_детали_seq    SEQUENCE     �   CREATE SEQUENCE public."детали_инвестиций_id_детали_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 N   DROP SEQUENCE public."детали_инвестиций_id_детали_seq";
       public               postgres    false    239            �           0    0 5   детали_инвестиций_id_детали_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."детали_инвестиций_id_детали_seq" OWNED BY public."детали_инвестиций"."id_детали";
          public               postgres    false    238            �            1259    16813 )   доходность_инвестиций    TABLE       CREATE TABLE public."доходность_инвестиций" (
    "id_доходности" integer NOT NULL,
    "id_портфеля" integer,
    "доходность" double precision,
    "дата_обновления" timestamp without time zone
);
 ?   DROP TABLE public."доходность_инвестиций";
       public         heap r       postgres    false            �            1259    16812 ?   доходность_инвести_id_доходности_seq    SEQUENCE     �   CREATE SEQUENCE public."доходность_инвести_id_доходности_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 X   DROP SEQUENCE public."доходность_инвести_id_доходности_seq";
       public               postgres    false    241            �           0    0 ?   доходность_инвести_id_доходности_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."доходность_инвести_id_доходности_seq" OWNED BY public."доходность_инвестиций"."id_доходности";
          public               postgres    false    240            �            1259    16765    инвестиции    TABLE     �   CREATE TABLE public."инвестиции" (
    "id_портфеля" integer NOT NULL,
    "id_клиента" integer,
    "баланс" integer,
    "дата_создания" timestamp without time zone,
    "статус" character varying
);
 *   DROP TABLE public."инвестиции";
       public         heap r       postgres    false            �            1259    16764 ,   инвестиции_id_портфеля_seq    SEQUENCE     �   CREATE SEQUENCE public."инвестиции_id_портфеля_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 E   DROP SEQUENCE public."инвестиции_id_портфеля_seq";
       public               postgres    false    235            �           0    0 ,   инвестиции_id_портфеля_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."инвестиции_id_портфеля_seq" OWNED BY public."инвестиции"."id_портфеля";
          public               postgres    false    234            �            1259    16691    клиент    TABLE     �  CREATE TABLE public."клиент" (
    "id_клиента" integer NOT NULL,
    email character varying,
    "фамилия" character varying,
    "имя" character varying,
    "отчество" character varying,
    "дата_создания" timestamp without time zone,
    "дата_обновление" timestamp without time zone,
    "id_роли" integer,
    "пароль" character varying,
    access_token character varying,
    refresh_token character varying
);
 "   DROP TABLE public."клиент";
       public         heap r       postgres    false            �            1259    16690 "   клиент_id_клиента_seq    SEQUENCE     �   CREATE SEQUENCE public."клиент_id_клиента_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public."клиент_id_клиента_seq";
       public               postgres    false    225            �           0    0 "   клиент_id_клиента_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public."клиент_id_клиента_seq" OWNED BY public."клиент"."id_клиента";
          public               postgres    false    224            �            1259    16673    операции    TABLE     �   CREATE TABLE public."операции" (
    "id_операции" integer NOT NULL,
    "название_операции" character varying
);
 &   DROP TABLE public."операции";
       public         heap r       postgres    false            �            1259    16672 (   операции_id_операции_seq    SEQUENCE     �   CREATE SEQUENCE public."операции_id_операции_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 A   DROP SEQUENCE public."операции_id_операции_seq";
       public               postgres    false    221            �           0    0 (   операции_id_операции_seq    SEQUENCE OWNED BY     {   ALTER SEQUENCE public."операции_id_операции_seq" OWNED BY public."операции"."id_операции";
          public               postgres    false    220            �            1259    16731 )   процентная_ставка_в_сч    TABLE       CREATE TABLE public."процентная_ставка_в_сч" (
    "id_процентной_ставки" integer NOT NULL,
    "процентная_ставка" integer,
    "id_вида_счета" integer,
    "дата_изменения" timestamp without time zone
);
 ?   DROP TABLE public."процентная_ставка_в_сч";
       public         heap r       postgres    false            �            1259    16730 >   процентная_став_id_процентной_ст_seq    SEQUENCE     �   CREATE SEQUENCE public."процентная_став_id_процентной_ст_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 W   DROP SEQUENCE public."процентная_став_id_процентной_ст_seq";
       public               postgres    false    231            �           0    0 >   процентная_став_id_процентной_ст_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."процентная_став_id_процентной_ст_seq" OWNED BY public."процентная_ставка_в_сч"."id_процентной_ставки";
          public               postgres    false    230            �            1259    16644    роли    TABLE     i   CREATE TABLE public."роли" (
    "id_роли" integer NOT NULL,
    "роль" character varying
);
    DROP TABLE public."роли";
       public         heap r       postgres    false            �            1259    16643    роли_id_роли_seq    SEQUENCE     �   CREATE SEQUENCE public."роли_id_роли_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."роли_id_роли_seq";
       public               postgres    false    215            �           0    0    роли_id_роли_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public."роли_id_роли_seq" OWNED BY public."роли"."id_роли";
          public               postgres    false    214            �            1259    16743    счет    TABLE       CREATE TABLE public."счет" (
    "id_счета" integer NOT NULL,
    "id_клиента" integer,
    "id_филиала" integer,
    "id_вида_счета" integer,
    "дата_открытия" timestamp without time zone,
    "баланс" bytea
);
    DROP TABLE public."счет";
       public         heap r       postgres    false            �            1259    16742    счет_id_счета_seq    SEQUENCE     �   CREATE SEQUENCE public."счет_id_счета_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public."счет_id_счета_seq";
       public               postgres    false    233            �           0    0    счет_id_счета_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public."счет_id_счета_seq" OWNED BY public."счет"."id_счета";
          public               postgres    false    232            �            1259    16664    тип_счета    TABLE     �   CREATE TABLE public."тип_счета" (
    "id_типа_счета" integer NOT NULL,
    "название_типа_счета" character varying
);
 '   DROP TABLE public."тип_счета";
       public         heap r       postgres    false            �            1259    16663 ,   тип_счета_id_типа_счета_seq    SEQUENCE     �   CREATE SEQUENCE public."тип_счета_id_типа_счета_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 E   DROP SEQUENCE public."тип_счета_id_типа_счета_seq";
       public               postgres    false    219            �           0    0 ,   тип_счета_id_типа_счета_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."тип_счета_id_типа_счета_seq" OWNED BY public."тип_счета"."id_типа_счета";
          public               postgres    false    218            �            1259    16682    типы_инвестиций    TABLE     �   CREATE TABLE public."типы_инвестиций" (
    "id_типа_инвестиций" integer NOT NULL,
    "название_типа" character varying
);
 3   DROP TABLE public."типы_инвестиций";
       public         heap r       postgres    false            �            1259    16681 >   типы_инвестиций_id_типа_инвестиц_seq    SEQUENCE     �   CREATE SEQUENCE public."типы_инвестиций_id_типа_инвестиц_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 W   DROP SEQUENCE public."типы_инвестиций_id_типа_инвестиц_seq";
       public               postgres    false    223            �           0    0 >   типы_инвестиций_id_типа_инвестиц_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."типы_инвестиций_id_типа_инвестиц_seq" OWNED BY public."типы_инвестиций"."id_типа_инвестиций";
          public               postgres    false    222            �            1259    16655 
   улица    TABLE     �   CREATE TABLE public."улица" (
    "id_улицы" integer NOT NULL,
    "название_улицы" character varying
);
     DROP TABLE public."улица";
       public         heap r       postgres    false            �            1259    16654    улица_id_улицы_seq    SEQUENCE     �   CREATE SEQUENCE public."улица_id_улицы_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public."улица_id_улицы_seq";
       public               postgres    false    217            �           0    0    улица_id_улицы_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public."улица_id_улицы_seq" OWNED BY public."улица"."id_улицы";
          public               postgres    false    216            �            1259    16705    филиал    TABLE     �   CREATE TABLE public."филиал" (
    "id_филиала" integer NOT NULL,
    "улица_филиала" integer,
    "дом_филиала" integer,
    "корпус_филиала" integer
);
 "   DROP TABLE public."филиал";
       public         heap r       postgres    false            �            1259    16704 "   филиал_id_филиала_seq    SEQUENCE     �   CREATE SEQUENCE public."филиал_id_филиала_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public."филиал_id_филиала_seq";
       public               postgres    false    227            �           0    0 "   филиал_id_филиала_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public."филиал_id_филиала_seq" OWNED BY public."филиал"."id_филиала";
          public               postgres    false    226            �           2604    16782 N   банковская_операция id_банковской_операции    DEFAULT     �   ALTER TABLE ONLY public."банковская_операция" ALTER COLUMN "id_банковской_операции" SET DEFAULT nextval('public."банковская_опер_id_банковской_оп_seq"'::regclass);
 �   ALTER TABLE public."банковская_операция" ALTER COLUMN "id_банковской_операции" DROP DEFAULT;
       public               postgres    false    236    237    237            �           2604    16720 (   вид_счета id_вида_счета    DEFAULT     �   ALTER TABLE ONLY public."вид_счета" ALTER COLUMN "id_вида_счета" SET DEFAULT nextval('public."вид_счета_id_вида_счета_seq"'::regclass);
 [   ALTER TABLE public."вид_счета" ALTER COLUMN "id_вида_счета" DROP DEFAULT;
       public               postgres    false    229    228    229            �           2604    16799 1   детали_инвестиций id_детали    DEFAULT     �   ALTER TABLE ONLY public."детали_инвестиций" ALTER COLUMN "id_детали" SET DEFAULT nextval('public."детали_инвестиций_id_детали_seq"'::regclass);
 d   ALTER TABLE public."детали_инвестиций" ALTER COLUMN "id_детали" DROP DEFAULT;
       public               postgres    false    238    239    239            �           2604    16816 A   доходность_инвестиций id_доходности    DEFAULT     �   ALTER TABLE ONLY public."доходность_инвестиций" ALTER COLUMN "id_доходности" SET DEFAULT nextval('public."доходность_инвести_id_доходности_seq"'::regclass);
 t   ALTER TABLE public."доходность_инвестиций" ALTER COLUMN "id_доходности" DROP DEFAULT;
       public               postgres    false    241    240    241            �           2604    16768 (   инвестиции id_портфеля    DEFAULT     �   ALTER TABLE ONLY public."инвестиции" ALTER COLUMN "id_портфеля" SET DEFAULT nextval('public."инвестиции_id_портфеля_seq"'::regclass);
 [   ALTER TABLE public."инвестиции" ALTER COLUMN "id_портфеля" DROP DEFAULT;
       public               postgres    false    234    235    235            �           2604    16694    клиент id_клиента    DEFAULT     �   ALTER TABLE ONLY public."клиент" ALTER COLUMN "id_клиента" SET DEFAULT nextval('public."клиент_id_клиента_seq"'::regclass);
 Q   ALTER TABLE public."клиент" ALTER COLUMN "id_клиента" DROP DEFAULT;
       public               postgres    false    225    224    225            �           2604    16676 $   операции id_операции    DEFAULT     �   ALTER TABLE ONLY public."операции" ALTER COLUMN "id_операции" SET DEFAULT nextval('public."операции_id_операции_seq"'::regclass);
 W   ALTER TABLE public."операции" ALTER COLUMN "id_операции" DROP DEFAULT;
       public               postgres    false    220    221    221            �           2604    16734 N   процентная_ставка_в_сч id_процентной_ставки    DEFAULT     �   ALTER TABLE ONLY public."процентная_ставка_в_сч" ALTER COLUMN "id_процентной_ставки" SET DEFAULT nextval('public."процентная_став_id_процентной_ст_seq"'::regclass);
 �   ALTER TABLE public."процентная_ставка_в_сч" ALTER COLUMN "id_процентной_ставки" DROP DEFAULT;
       public               postgres    false    230    231    231            �           2604    16647    роли id_роли    DEFAULT     �   ALTER TABLE ONLY public."роли" ALTER COLUMN "id_роли" SET DEFAULT nextval('public."роли_id_роли_seq"'::regclass);
 G   ALTER TABLE public."роли" ALTER COLUMN "id_роли" DROP DEFAULT;
       public               postgres    false    215    214    215            �           2604    16746    счет id_счета    DEFAULT     �   ALTER TABLE ONLY public."счет" ALTER COLUMN "id_счета" SET DEFAULT nextval('public."счет_id_счета_seq"'::regclass);
 I   ALTER TABLE public."счет" ALTER COLUMN "id_счета" DROP DEFAULT;
       public               postgres    false    233    232    233            �           2604    16667 (   тип_счета id_типа_счета    DEFAULT     �   ALTER TABLE ONLY public."тип_счета" ALTER COLUMN "id_типа_счета" SET DEFAULT nextval('public."тип_счета_id_типа_счета_seq"'::regclass);
 [   ALTER TABLE public."тип_счета" ALTER COLUMN "id_типа_счета" DROP DEFAULT;
       public               postgres    false    219    218    219            �           2604    16685 >   типы_инвестиций id_типа_инвестиций    DEFAULT     �   ALTER TABLE ONLY public."типы_инвестиций" ALTER COLUMN "id_типа_инвестиций" SET DEFAULT nextval('public."типы_инвестиций_id_типа_инвестиц_seq"'::regclass);
 q   ALTER TABLE public."типы_инвестиций" ALTER COLUMN "id_типа_инвестиций" DROP DEFAULT;
       public               postgres    false    222    223    223            �           2604    16658    улица id_улицы    DEFAULT     �   ALTER TABLE ONLY public."улица" ALTER COLUMN "id_улицы" SET DEFAULT nextval('public."улица_id_улицы_seq"'::regclass);
 K   ALTER TABLE public."улица" ALTER COLUMN "id_улицы" DROP DEFAULT;
       public               postgres    false    217    216    217            �           2604    16708    филиал id_филиала    DEFAULT     �   ALTER TABLE ONLY public."филиал" ALTER COLUMN "id_филиала" SET DEFAULT nextval('public."филиал_id_филиала_seq"'::regclass);
 Q   ALTER TABLE public."филиал" ALTER COLUMN "id_филиала" DROP DEFAULT;
       public               postgres    false    226    227    227            �          0    24792    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    242   y�       �          0    16779 %   банковская_операция 
   TABLE DATA           �   COPY public."банковская_операция" ("id_банковской_операции", "id_счета", "сумма", "id_операции") FROM stdin;
    public               postgres    false    237   ��       �          0    16717    вид_счета 
   TABLE DATA           �   COPY public."вид_счета" ("id_вида_счета", "название_вида_счета", "id_типа_счета") FROM stdin;
    public               postgres    false    229   ��       �          0    16796 !   детали_инвестиций 
   TABLE DATA           �   COPY public."детали_инвестиций" ("id_детали", "id_портфеля", "id_типа_инвестиций", "сумма", "дата_покупки") FROM stdin;
    public               postgres    false    239   g�       �          0    16813 )   доходность_инвестиций 
   TABLE DATA           �   COPY public."доходность_инвестиций" ("id_доходности", "id_портфеля", "доходность", "дата_обновления") FROM stdin;
    public               postgres    false    241   ��       �          0    16765    инвестиции 
   TABLE DATA           �   COPY public."инвестиции" ("id_портфеля", "id_клиента", "баланс", "дата_создания", "статус") FROM stdin;
    public               postgres    false    235   �       �          0    16691    клиент 
   TABLE DATA           �   COPY public."клиент" ("id_клиента", email, "фамилия", "имя", "отчество", "дата_создания", "дата_обновление", "id_роли", "пароль", access_token, refresh_token) FROM stdin;
    public               postgres    false    225   ?�       �          0    16673    операции 
   TABLE DATA           h   COPY public."операции" ("id_операции", "название_операции") FROM stdin;
    public               postgres    false    221   /�       �          0    16731 )   процентная_ставка_в_сч 
   TABLE DATA           �   COPY public."процентная_ставка_в_сч" ("id_процентной_ставки", "процентная_ставка", "id_вида_счета", "дата_изменения") FROM stdin;
    public               postgres    false    231   {�       �          0    16644    роли 
   TABLE DATA           ?   COPY public."роли" ("id_роли", "роль") FROM stdin;
    public               postgres    false    215   ��       �          0    16743    счет 
   TABLE DATA           �   COPY public."счет" ("id_счета", "id_клиента", "id_филиала", "id_вида_счета", "дата_открытия", "баланс") FROM stdin;
    public               postgres    false    233   �       �          0    16664    тип_счета 
   TABLE DATA           o   COPY public."тип_счета" ("id_типа_счета", "название_типа_счета") FROM stdin;
    public               postgres    false    219   Ǽ       �          0    16682    типы_инвестиций 
   TABLE DATA           z   COPY public."типы_инвестиций" ("id_типа_инвестиций", "название_типа") FROM stdin;
    public               postgres    false    223   	�       �          0    16655 
   улица 
   TABLE DATA           V   COPY public."улица" ("id_улицы", "название_улицы") FROM stdin;
    public               postgres    false    217   E�       �          0    16705    филиал 
   TABLE DATA           �   COPY public."филиал" ("id_филиала", "улица_филиала", "дом_филиала", "корпус_филиала") FROM stdin;
    public               postgres    false    227   ��       �           0    0 >   банковская_опер_id_банковской_оп_seq    SEQUENCE SET     o   SELECT pg_catalog.setval('public."банковская_опер_id_банковской_оп_seq"', 12, true);
          public               postgres    false    236            �           0    0 ,   вид_счета_id_вида_счета_seq    SEQUENCE SET     \   SELECT pg_catalog.setval('public."вид_счета_id_вида_счета_seq"', 5, true);
          public               postgres    false    228            �           0    0 5   детали_инвестиций_id_детали_seq    SEQUENCE SET     e   SELECT pg_catalog.setval('public."детали_инвестиций_id_детали_seq"', 2, true);
          public               postgres    false    238            �           0    0 ?   доходность_инвести_id_доходности_seq    SEQUENCE SET     o   SELECT pg_catalog.setval('public."доходность_инвести_id_доходности_seq"', 2, true);
          public               postgres    false    240            �           0    0 ,   инвестиции_id_портфеля_seq    SEQUENCE SET     \   SELECT pg_catalog.setval('public."инвестиции_id_портфеля_seq"', 1, true);
          public               postgres    false    234            �           0    0 "   клиент_id_клиента_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public."клиент_id_клиента_seq"', 12, true);
          public               postgres    false    224            �           0    0 (   операции_id_операции_seq    SEQUENCE SET     Y   SELECT pg_catalog.setval('public."операции_id_операции_seq"', 1, false);
          public               postgres    false    220            �           0    0 >   процентная_став_id_процентной_ст_seq    SEQUENCE SET     n   SELECT pg_catalog.setval('public."процентная_став_id_процентной_ст_seq"', 1, true);
          public               postgres    false    230            �           0    0    роли_id_роли_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public."роли_id_роли_seq"', 2, true);
          public               postgres    false    214            �           0    0    счет_id_счета_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public."счет_id_счета_seq"', 10, true);
          public               postgres    false    232            �           0    0 ,   тип_счета_id_типа_счета_seq    SEQUENCE SET     ]   SELECT pg_catalog.setval('public."тип_счета_id_типа_счета_seq"', 1, false);
          public               postgres    false    218            �           0    0 >   типы_инвестиций_id_типа_инвестиц_seq    SEQUENCE SET     o   SELECT pg_catalog.setval('public."типы_инвестиций_id_типа_инвестиц_seq"', 1, false);
          public               postgres    false    222            �           0    0    улица_id_улицы_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public."улица_id_улицы_seq"', 3, true);
          public               postgres    false    216            �           0    0 "   филиал_id_филиала_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public."филиал_id_филиала_seq"', 3, true);
          public               postgres    false    226            �           2606    24796 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    242            �           2606    16784 P   банковская_операция банковская_операция_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."банковская_операция"
    ADD CONSTRAINT "банковская_операция_pkey" PRIMARY KEY ("id_банковской_операции");
 ~   ALTER TABLE ONLY public."банковская_операция" DROP CONSTRAINT "банковская_операция_pkey";
       public                 postgres    false    237            �           2606    16724 (   вид_счета вид_счета_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."вид_счета"
    ADD CONSTRAINT "вид_счета_pkey" PRIMARY KEY ("id_вида_счета");
 V   ALTER TABLE ONLY public."вид_счета" DROP CONSTRAINT "вид_счета_pkey";
       public                 postgres    false    229            �           2606    16801 H   детали_инвестиций детали_инвестиций_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."детали_инвестиций"
    ADD CONSTRAINT "детали_инвестиций_pkey" PRIMARY KEY ("id_детали");
 v   ALTER TABLE ONLY public."детали_инвестиций" DROP CONSTRAINT "детали_инвестиций_pkey";
       public                 postgres    false    239            �           2606    16818 X   доходность_инвестиций доходность_инвестиций_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."доходность_инвестиций"
    ADD CONSTRAINT "доходность_инвестиций_pkey" PRIMARY KEY ("id_доходности");
 �   ALTER TABLE ONLY public."доходность_инвестиций" DROP CONSTRAINT "доходность_инвестиций_pkey";
       public                 postgres    false    241            �           2606    16772 .   инвестиции инвестиции_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."инвестиции"
    ADD CONSTRAINT "инвестиции_pkey" PRIMARY KEY ("id_портфеля");
 \   ALTER TABLE ONLY public."инвестиции" DROP CONSTRAINT "инвестиции_pkey";
       public                 postgres    false    235            �           2606    16698    клиент клиент_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT "клиент_pkey" PRIMARY KEY ("id_клиента");
 L   ALTER TABLE ONLY public."клиент" DROP CONSTRAINT "клиент_pkey";
       public                 postgres    false    225            �           2606    16680 &   операции операции_pkey 
   CONSTRAINT     {   ALTER TABLE ONLY public."операции"
    ADD CONSTRAINT "операции_pkey" PRIMARY KEY ("id_операции");
 T   ALTER TABLE ONLY public."операции" DROP CONSTRAINT "операции_pkey";
       public                 postgres    false    221            �           2606    16736 X   процентная_ставка_в_сч процентная_ставка_в_сч_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."процентная_ставка_в_сч"
    ADD CONSTRAINT "процентная_ставка_в_сч_pkey" PRIMARY KEY ("id_процентной_ставки");
 �   ALTER TABLE ONLY public."процентная_ставка_в_сч" DROP CONSTRAINT "процентная_ставка_в_сч_pkey";
       public                 postgres    false    231            �           2606    16651    роли роли_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public."роли"
    ADD CONSTRAINT "роли_pkey" PRIMARY KEY ("id_роли");
 D   ALTER TABLE ONLY public."роли" DROP CONSTRAINT "роли_pkey";
       public                 postgres    false    215            �           2606    16653    роли роли_роль_key 
   CONSTRAINT     c   ALTER TABLE ONLY public."роли"
    ADD CONSTRAINT "роли_роль_key" UNIQUE ("роль");
 L   ALTER TABLE ONLY public."роли" DROP CONSTRAINT "роли_роль_key";
       public                 postgres    false    215            �           2606    16748    счет счет_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_pkey" PRIMARY KEY ("id_счета");
 D   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_pkey";
       public                 postgres    false    233            �           2606    16671 (   тип_счета тип_счета_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."тип_счета"
    ADD CONSTRAINT "тип_счета_pkey" PRIMARY KEY ("id_типа_счета");
 V   ALTER TABLE ONLY public."тип_счета" DROP CONSTRAINT "тип_счета_pkey";
       public                 postgres    false    219            �           2606    16689 @   типы_инвестиций типы_инвестиций_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."типы_инвестиций"
    ADD CONSTRAINT "типы_инвестиций_pkey" PRIMARY KEY ("id_типа_инвестиций");
 n   ALTER TABLE ONLY public."типы_инвестиций" DROP CONSTRAINT "типы_инвестиций_pkey";
       public                 postgres    false    223            �           2606    16662    улица улица_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public."улица"
    ADD CONSTRAINT "улица_pkey" PRIMARY KEY ("id_улицы");
 H   ALTER TABLE ONLY public."улица" DROP CONSTRAINT "улица_pkey";
       public                 postgres    false    217            �           2606    16710    филиал филиал_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public."филиал"
    ADD CONSTRAINT "филиал_pkey" PRIMARY KEY ("id_филиала");
 L   ALTER TABLE ONLY public."филиал" DROP CONSTRAINT "филиал_pkey";
       public                 postgres    false    227            �           1259    24797    ix_клиент_email    INDEX     Z   CREATE UNIQUE INDEX "ix_клиент_email" ON public."клиент" USING btree (email);
 +   DROP INDEX public."ix_клиент_email";
       public                 postgres    false    225            �           1259    24798 !   ix_клиент_id_клиента    INDEX     m   CREATE INDEX "ix_клиент_id_клиента" ON public."клиент" USING btree ("id_клиента");
 7   DROP INDEX public."ix_клиент_id_клиента";
       public                 postgres    false    225            �           2606    16790 d   банковская_операция банковская_операция_id_операции_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."банковская_операция"
    ADD CONSTRAINT "банковская_операция_id_операции_fkey" FOREIGN KEY ("id_операции") REFERENCES public."операции"("id_операции");
 �   ALTER TABLE ONLY public."банковская_операция" DROP CONSTRAINT "банковская_операция_id_операции_fkey";
       public               postgres    false    237    221    3291            �           2606    16785 ^   банковская_операция банковская_операция_id_счета_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."банковская_операция"
    ADD CONSTRAINT "банковская_операция_id_счета_fkey" FOREIGN KEY ("id_счета") REFERENCES public."счет"("id_счета");
 �   ALTER TABLE ONLY public."банковская_операция" DROP CONSTRAINT "банковская_операция_id_счета_fkey";
       public               postgres    false    3305    237    233            �           2606    16725 ?   вид_счета вид_счета_id_типа_счета_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."вид_счета"
    ADD CONSTRAINT "вид_счета_id_типа_счета_fkey" FOREIGN KEY ("id_типа_счета") REFERENCES public."тип_счета"("id_типа_счета");
 m   ALTER TABLE ONLY public."вид_счета" DROP CONSTRAINT "вид_счета_id_типа_счета_fkey";
       public               postgres    false    229    219    3289            �           2606    16807 a   детали_инвестиций детали_инвестиц_id_типа_инвестиц_fkey    FK CONSTRAINT       ALTER TABLE ONLY public."детали_инвестиций"
    ADD CONSTRAINT "детали_инвестиц_id_типа_инвестиц_fkey" FOREIGN KEY ("id_типа_инвестиций") REFERENCES public."типы_инвестиций"("id_типа_инвестиций");
 �   ALTER TABLE ONLY public."детали_инвестиций" DROP CONSTRAINT "детали_инвестиц_id_типа_инвестиц_fkey";
       public               postgres    false    223    239    3293            �           2606    16802 \   детали_инвестиций детали_инвестиций_id_портфеля_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."детали_инвестиций"
    ADD CONSTRAINT "детали_инвестиций_id_портфеля_fkey" FOREIGN KEY ("id_портфеля") REFERENCES public."инвестиции"("id_портфеля");
 �   ALTER TABLE ONLY public."детали_инвестиций" DROP CONSTRAINT "детали_инвестиций_id_портфеля_fkey";
       public               postgres    false    3307    235    239                        2606    16819 h   доходность_инвестиций доходность_инвестиц_id_портфеля_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."доходность_инвестиций"
    ADD CONSTRAINT "доходность_инвестиц_id_портфеля_fkey" FOREIGN KEY ("id_портфеля") REFERENCES public."инвестиции"("id_портфеля");
 �   ALTER TABLE ONLY public."доходность_инвестиций" DROP CONSTRAINT "доходность_инвестиц_id_портфеля_fkey";
       public               postgres    false    235    241    3307            �           2606    16773 @   инвестиции инвестиции_id_клиента_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."инвестиции"
    ADD CONSTRAINT "инвестиции_id_клиента_fkey" FOREIGN KEY ("id_клиента") REFERENCES public."клиент"("id_клиента");
 n   ALTER TABLE ONLY public."инвестиции" DROP CONSTRAINT "инвестиции_id_клиента_fkey";
       public               postgres    false    3297    225    235            �           2606    16699 *   клиент клиент_id_роли_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT "клиент_id_роли_fkey" FOREIGN KEY ("id_роли") REFERENCES public."роли"("id_роли");
 X   ALTER TABLE ONLY public."клиент" DROP CONSTRAINT "клиент_id_роли_fkey";
       public               postgres    false    3283    215    225            �           2606    16737 h   процентная_ставка_в_сч процентная_ставка__id_вида_счета_fkey    FK CONSTRAINT        ALTER TABLE ONLY public."процентная_ставка_в_сч"
    ADD CONSTRAINT "процентная_ставка__id_вида_счета_fkey" FOREIGN KEY ("id_вида_счета") REFERENCES public."вид_счета"("id_вида_счета");
 �   ALTER TABLE ONLY public."процентная_ставка_в_сч" DROP CONSTRAINT "процентная_ставка__id_вида_счета_fkey";
       public               postgres    false    229    3301    231            �           2606    16759 -   счет счет_id_вида_счета_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_id_вида_счета_fkey" FOREIGN KEY ("id_вида_счета") REFERENCES public."вид_счета"("id_вида_счета");
 [   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_id_вида_счета_fkey";
       public               postgres    false    229    3301    233            �           2606    16749 (   счет счет_id_клиента_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_id_клиента_fkey" FOREIGN KEY ("id_клиента") REFERENCES public."клиент"("id_клиента");
 V   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_id_клиента_fkey";
       public               postgres    false    233    3297    225            �           2606    16754 (   счет счет_id_филиала_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_id_филиала_fkey" FOREIGN KEY ("id_филиала") REFERENCES public."филиал"("id_филиала");
 V   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_id_филиала_fkey";
       public               postgres    false    3299    233    227            �           2606    16711 8   филиал филиал_улица_филиала_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."филиал"
    ADD CONSTRAINT "филиал_улица_филиала_fkey" FOREIGN KEY ("улица_филиала") REFERENCES public."улица"("id_улицы");
 f   ALTER TABLE ONLY public."филиал" DROP CONSTRAINT "филиал_улица_филиала_fkey";
       public               postgres    false    227    3287    217            �      x�3J5KMM631154����� ,��      �   A   x�5���0Cѳ�K<@bzI�u���|�ナ@��ԛO/ֈ�l�i���T`S�'[}��Fr {�6      �   c   x�e��@@DϻU�@B�F1�8��I	Kll�jx�#s�9��?/S;V�J�k���lD�]�Ǣ:r�Ԑ	�l3IN�w�æ_����D�ܕ��p>J{      �   =   x�]���@��P��,{�9R���!~�䗤�P�ԉ��;�*�t�~Ǟ�X!n��_ġV      �   -   x�3�4�40�4202�5 !s+S+=sCccC�=... �4�      �   >   x�3�44 "N##S] 2Q04�20�20�3�0�0�®�Mv\�ta���;�b���� �wT      �   �  x���ˎ�V���S̢���ثi�.6`���"���b�m0`V�l�
�E��(�f�y��bwO2�2R"��ꯒ~��)�:E�o7�e���l�i?�����Ϗ������(�Q�O�?u@�-�oQ� � P CL��$عA�D7�o����
b�,.řsn�9��he�	��jP�}���t������Np�CO�#-�%���I���()���P�S��f���C��U���Yl��N-=㲰���2��:O��*�Թ�yR��B2�܍xȧ��L��(�J1�#u=1�
Fb�Q�ѓ��++�հ�\L�5��%��r��s-g��e�e:u!x����~<s����c��3�/ŋ����� 3��h�e�� ��^	BB���*vFG��P(��y�|�I�ũyl(��P��I<�eз�8JB�78�v����~!EU��a%�Y�6:��I�4~�֩�n콣蜷��x�k�y0	�S���D��"�|�m^���(��O^�rT�����I�.���v��_���~���D��.��}P������Fy���������/ŋ�,!0d�p������Yjk���2�O���C���]o%��j	���;$��Ʈ'������*מ�=�}�~���K��~�
���J�n�`����yRd��evIx�& �s���8�h��:�'C�� PS�m�y���!�0-��r{0v�ʘ�ƽ����v�6o�0      �   <   x�3�0�¾��x�����[��8/,���b��&0��j����&��-\1z\\\ �l#�      �   .   x�3�4��4�4202�50�52V00�20�24г0741����� ~�w      �   *   x�3估���;.l���b���\������� N��      �   �   x�mλ��@DQ����/��GRw�0�/ػ��g��iÍ6�ȇ��b�8dU����<��4�$	}�l$�lXEj�qC*M�5;V�D��=6���p>�ס���l��76J"�Zކ3�T�[OˁX�s,H��=%��y!�Ki~��T
?�C�C�p�FbfW(���n��"�2�F��<�������l N"      �   2   x�' ��1	кредитный
2	вклад
\.


�V�      �   ,   x�3�0�®�mv\��2�0����/츰���`� ˬ�      �   Q   x�Ƚ	�0F�:o
'��8L��`aag�Q	��;�o#S��o*^�b�ƣ��]A���Uwᤑ�A�α�8I
\|����~�%))      �      x�3�4�44�4�2�4�46�4����� #��     