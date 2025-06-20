PGDMP                       }            vip_bank     15.12 (Debian 15.12-1.pgdg120+1)    17.0 l    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16605    vip_bank    DATABASE     s   CREATE DATABASE vip_bank WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE vip_bank;
                     postgres    false                        3079    49383    pgcrypto 	   EXTENSION     <   CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;
    DROP EXTENSION pgcrypto;
                        false            �           0    0    EXTENSION pgcrypto    COMMENT     <   COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';
                             false    2                       1255    49422    check_non_negative_balance()    FUNCTION     	  CREATE FUNCTION public.check_non_negative_balance() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.баланс < 0 THEN
    RAISE EXCEPTION 'Баланс не может быть отрицательным.';
  END IF;
  RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.check_non_negative_balance();
       public               postgres    false                        1255    49424    check_transfer_conditions()    FUNCTION     E  CREATE FUNCTION public.check_transfer_conditions() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    баланс_отправителя NUMERIC;
BEGIN
    IF NEW.сумма <= 0 THEN
        RAISE EXCEPTION 'Сумма перевода должна быть положительной.';
    END IF;

    SELECT баланс INTO баланс_отправителя FROM счет WHERE id_счета = NEW.id_счета;

    IF баланс_отправителя IS NULL THEN
        RAISE EXCEPTION 'Счёт отправителя не найден.';
    END IF;

    IF NEW.сумма < 0 AND баланс_отправителя < ABS(NEW.сумма) THEN
        RAISE EXCEPTION 'Недостаточно средств на счете отправителя.';
    END IF;

    RETURN NEW;
END;
$$;
 2   DROP FUNCTION public.check_transfer_conditions();
       public               postgres    false            !           1255    49430    check_unique_email()    FUNCTION     �  CREATE FUNCTION public.check_unique_email() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM клиент
        WHERE email = NEW.email AND id_клиента <> COALESCE(NEW.id_клиента, -1)
    ) THEN
        RAISE EXCEPTION 'Клиент с email "%" уже существует.', NEW.email;
    END IF;
    RETURN NEW;
END;
$$;
 +   DROP FUNCTION public.check_unique_email();
       public               postgres    false                       1255    49420    hash_password_if_needed()    FUNCTION        CREATE FUNCTION public.hash_password_if_needed() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
  IF NEW.пароль IS NOT NULL AND NEW.пароль !~ '^\\$2[aby]\\$' THEN
    NEW.пароль := crypt(NEW.пароль, gen_salt('bf'));
  END IF;
  RETURN NEW;
END;
$_$;
 0   DROP FUNCTION public.hash_password_if_needed();
       public               postgres    false                       1255    49423 "   prevent_multiple_credit_accounts()    FUNCTION     �  CREATE FUNCTION public.prevent_multiple_credit_accounts() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  тип_счета INT;
BEGIN
  SELECT id_типа_счета INTO тип_счета FROM вид_счета WHERE id_вида_счета = NEW.id_вида_счета;

  IF тип_счета = 1 THEN
    IF EXISTS (
      SELECT 1 FROM счет s
      JOIN вид_счета vs ON s.id_вида_счета = vs.id_вида_счета
      WHERE s.id_клиента = NEW.id_клиента AND vs.id_типа_счета = 1
    ) THEN
      RAISE EXCEPTION 'Нельзя открыть более одного кредитного счёта для клиента.';
    END IF;
  END IF;

  RETURN NEW;
END;
$$;
 9   DROP FUNCTION public.prevent_multiple_credit_accounts();
       public               postgres    false                       1255    49421    validate_password_trigger()    FUNCTION     �  CREATE FUNCTION public.validate_password_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
  IF length(NEW.пароль) < 8 THEN
    RAISE EXCEPTION 'Пароль должен содержать минимум 8 символов.';
  END IF;

  IF NEW.пароль !~ '[A-Z]' THEN
    RAISE EXCEPTION 'Пароль должен содержать хотя бы одну заглавную букву.';
  END IF;

  IF NEW.пароль !~ '[a-z]' THEN
    RAISE EXCEPTION 'Пароль должен содержать хотя бы одну строчную букву.';
  END IF;

  IF NEW.пароль !~ '\d' THEN
    RAISE EXCEPTION 'Пароль должен содержать хотя бы одну цифру.';
  END IF;

  IF NEW.пароль !~ '[!@#$%^&*(),.?":{}|<>]' THEN
    RAISE EXCEPTION 'Пароль должен содержать хотя бы один специальный символ.';
  END IF;

  RETURN NEW;
END;
$_$;
 2   DROP FUNCTION public.validate_password_trigger();
       public               postgres    false            �            1259    24792    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    16691    клиент    TABLE     *  CREATE TABLE public."клиент" (
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

ALTER TABLE ONLY public."клиент" FORCE ROW LEVEL SECURITY;
 "   DROP TABLE public."клиент";
       public         heap r       postgres    false            �           0    0    TABLE "клиент"    ACL     �   GRANT SELECT ON TABLE public."клиент" TO rls_user;
GRANT SELECT ON TABLE public."клиент" TO "elenova@list.ru";
GRANT SELECT ON TABLE public."клиент" TO "nikolaev_nik@gmail.com";
          public               postgres    false    224            �            1259    49437    operator_info    VIEW     �   CREATE VIEW public.operator_info AS
 SELECT "клиент".email,
    "клиент"."id_роли"
   FROM public."клиент";
     DROP VIEW public.operator_info;
       public       v       postgres    false    224    224            �           0    0    TABLE operator_info    ACL     6   GRANT SELECT ON TABLE public.operator_info TO PUBLIC;
          public               postgres    false    236            �            1259    16779 %   банковская_операция    TABLE       CREATE TABLE public."банковская_операция" (
    "id_банковской_операции" integer NOT NULL,
    "id_счета" integer,
    "сумма" integer,
    "id_операции" integer,
    "дата_операции" timestamp without time zone
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
       public               postgres    false    234            �           0    0 >   банковская_опер_id_банковской_оп_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."банковская_опер_id_банковской_оп_seq" OWNED BY public."банковская_операция"."id_банковской_операции";
          public               postgres    false    233            �            1259    16717    вид_счета    TABLE     �   CREATE TABLE public."вид_счета" (
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
       public               postgres    false    228            �           0    0 ,   вид_счета_id_вида_счета_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."вид_счета_id_вида_счета_seq" OWNED BY public."вид_счета"."id_вида_счета";
          public               postgres    false    227            �            1259    16690 "   клиент_id_клиента_seq    SEQUENCE     �   CREATE SEQUENCE public."клиент_id_клиента_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public."клиент_id_клиента_seq";
       public               postgres    false    224            �           0    0 "   клиент_id_клиента_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public."клиент_id_клиента_seq" OWNED BY public."клиент"."id_клиента";
          public               postgres    false    223            �            1259    16673    операции    TABLE     �   CREATE TABLE public."операции" (
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
       public               postgres    false    222            �           0    0 (   операции_id_операции_seq    SEQUENCE OWNED BY     {   ALTER SEQUENCE public."операции_id_операции_seq" OWNED BY public."операции"."id_операции";
          public               postgres    false    221            �            1259    16731 )   процентная_ставка_в_сч    TABLE       CREATE TABLE public."процентная_ставка_в_сч" (
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
       public               postgres    false    230            �           0    0 >   процентная_став_id_процентной_ст_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."процентная_став_id_процентной_ст_seq" OWNED BY public."процентная_ставка_в_сч"."id_процентной_ставки";
          public               postgres    false    229            �            1259    16644    роли    TABLE     i   CREATE TABLE public."роли" (
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
       public               postgres    false    216            �           0    0    роли_id_роли_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public."роли_id_роли_seq" OWNED BY public."роли"."id_роли";
          public               postgres    false    215            �            1259    16743    счет    TABLE       CREATE TABLE public."счет" (
    "id_счета" integer NOT NULL,
    "id_клиента" integer,
    "id_филиала" integer,
    "id_вида_счета" integer,
    "дата_открытия" timestamp without time zone,
    "баланс" bytea NOT NULL
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
       public               postgres    false    232            �           0    0    счет_id_счета_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public."счет_id_счета_seq" OWNED BY public."счет"."id_счета";
          public               postgres    false    231            �            1259    16664    тип_счета    TABLE     �   CREATE TABLE public."тип_счета" (
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
       public               postgres    false    220            �           0    0 ,   тип_счета_id_типа_счета_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."тип_счета_id_типа_счета_seq" OWNED BY public."тип_счета"."id_типа_счета";
          public               postgres    false    219            �            1259    16655 
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
       public               postgres    false    218            �           0    0    улица_id_улицы_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public."улица_id_улицы_seq" OWNED BY public."улица"."id_улицы";
          public               postgres    false    217            �            1259    16705    филиал    TABLE     �   CREATE TABLE public."филиал" (
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
       public               postgres    false    226            �           0    0 "   филиал_id_филиала_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public."филиал_id_филиала_seq" OWNED BY public."филиал"."id_филиала";
          public               postgres    false    225            �           2604    16782 N   банковская_операция id_банковской_операции    DEFAULT     �   ALTER TABLE ONLY public."банковская_операция" ALTER COLUMN "id_банковской_операции" SET DEFAULT nextval('public."банковская_опер_id_банковской_оп_seq"'::regclass);
 �   ALTER TABLE public."банковская_операция" ALTER COLUMN "id_банковской_операции" DROP DEFAULT;
       public               postgres    false    234    233    234            �           2604    16720 (   вид_счета id_вида_счета    DEFAULT     �   ALTER TABLE ONLY public."вид_счета" ALTER COLUMN "id_вида_счета" SET DEFAULT nextval('public."вид_счета_id_вида_счета_seq"'::regclass);
 [   ALTER TABLE public."вид_счета" ALTER COLUMN "id_вида_счета" DROP DEFAULT;
       public               postgres    false    228    227    228            �           2604    16694    клиент id_клиента    DEFAULT     �   ALTER TABLE ONLY public."клиент" ALTER COLUMN "id_клиента" SET DEFAULT nextval('public."клиент_id_клиента_seq"'::regclass);
 Q   ALTER TABLE public."клиент" ALTER COLUMN "id_клиента" DROP DEFAULT;
       public               postgres    false    223    224    224            �           2604    16676 $   операции id_операции    DEFAULT     �   ALTER TABLE ONLY public."операции" ALTER COLUMN "id_операции" SET DEFAULT nextval('public."операции_id_операции_seq"'::regclass);
 W   ALTER TABLE public."операции" ALTER COLUMN "id_операции" DROP DEFAULT;
       public               postgres    false    221    222    222            �           2604    16734 N   процентная_ставка_в_сч id_процентной_ставки    DEFAULT     �   ALTER TABLE ONLY public."процентная_ставка_в_сч" ALTER COLUMN "id_процентной_ставки" SET DEFAULT nextval('public."процентная_став_id_процентной_ст_seq"'::regclass);
 �   ALTER TABLE public."процентная_ставка_в_сч" ALTER COLUMN "id_процентной_ставки" DROP DEFAULT;
       public               postgres    false    229    230    230            �           2604    16647    роли id_роли    DEFAULT     �   ALTER TABLE ONLY public."роли" ALTER COLUMN "id_роли" SET DEFAULT nextval('public."роли_id_роли_seq"'::regclass);
 G   ALTER TABLE public."роли" ALTER COLUMN "id_роли" DROP DEFAULT;
       public               postgres    false    216    215    216            �           2604    16746    счет id_счета    DEFAULT     �   ALTER TABLE ONLY public."счет" ALTER COLUMN "id_счета" SET DEFAULT nextval('public."счет_id_счета_seq"'::regclass);
 I   ALTER TABLE public."счет" ALTER COLUMN "id_счета" DROP DEFAULT;
       public               postgres    false    231    232    232            �           2604    16667 (   тип_счета id_типа_счета    DEFAULT     �   ALTER TABLE ONLY public."тип_счета" ALTER COLUMN "id_типа_счета" SET DEFAULT nextval('public."тип_счета_id_типа_счета_seq"'::regclass);
 [   ALTER TABLE public."тип_счета" ALTER COLUMN "id_типа_счета" DROP DEFAULT;
       public               postgres    false    220    219    220            �           2604    16658    улица id_улицы    DEFAULT     �   ALTER TABLE ONLY public."улица" ALTER COLUMN "id_улицы" SET DEFAULT nextval('public."улица_id_улицы_seq"'::regclass);
 K   ALTER TABLE public."улица" ALTER COLUMN "id_улицы" DROP DEFAULT;
       public               postgres    false    218    217    218            �           2604    16708    филиал id_филиала    DEFAULT     �   ALTER TABLE ONLY public."филиал" ALTER COLUMN "id_филиала" SET DEFAULT nextval('public."филиал_id_филиала_seq"'::regclass);
 Q   ALTER TABLE public."филиал" ALTER COLUMN "id_филиала" DROP DEFAULT;
       public               postgres    false    225    226    226            �          0    24792    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    235   ��       �          0    16779 %   банковская_операция 
   TABLE DATA           �   COPY public."банковская_операция" ("id_банковской_операции", "id_счета", "сумма", "id_операции", "дата_операции") FROM stdin;
    public               postgres    false    234   Ϧ       �          0    16717    вид_счета 
   TABLE DATA           �   COPY public."вид_счета" ("id_вида_счета", "название_вида_счета", "id_типа_счета") FROM stdin;
    public               postgres    false    228   s�       �          0    16691    клиент 
   TABLE DATA           �   COPY public."клиент" ("id_клиента", email, "фамилия", "имя", "отчество", "дата_создания", "дата_обновление", "id_роли", "пароль", access_token, refresh_token) FROM stdin;
    public               postgres    false    224   "�       �          0    16673    операции 
   TABLE DATA           h   COPY public."операции" ("id_операции", "название_операции") FROM stdin;
    public               postgres    false    222   t�       �          0    16731 )   процентная_ставка_в_сч 
   TABLE DATA           �   COPY public."процентная_ставка_в_сч" ("id_процентной_ставки", "процентная_ставка", "id_вида_счета", "дата_изменения") FROM stdin;
    public               postgres    false    230   ��       �          0    16644    роли 
   TABLE DATA           ?   COPY public."роли" ("id_роли", "роль") FROM stdin;
    public               postgres    false    216   8�       �          0    16743    счет 
   TABLE DATA           �   COPY public."счет" ("id_счета", "id_клиента", "id_филиала", "id_вида_счета", "дата_открытия", "баланс") FROM stdin;
    public               postgres    false    232   ��       �          0    16664    тип_счета 
   TABLE DATA           o   COPY public."тип_счета" ("id_типа_счета", "название_типа_счета") FROM stdin;
    public               postgres    false    220   ��       �          0    16655 
   улица 
   TABLE DATA           V   COPY public."улица" ("id_улицы", "название_улицы") FROM stdin;
    public               postgres    false    218   	�       �          0    16705    филиал 
   TABLE DATA           �   COPY public."филиал" ("id_филиала", "улица_филиала", "дом_филиала", "корпус_филиала") FROM stdin;
    public               postgres    false    226   j�       �           0    0 >   банковская_опер_id_банковской_оп_seq    SEQUENCE SET     o   SELECT pg_catalog.setval('public."банковская_опер_id_банковской_оп_seq"', 13, true);
          public               postgres    false    233            �           0    0 ,   вид_счета_id_вида_счета_seq    SEQUENCE SET     \   SELECT pg_catalog.setval('public."вид_счета_id_вида_счета_seq"', 8, true);
          public               postgres    false    227            �           0    0 "   клиент_id_клиента_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public."клиент_id_клиента_seq"', 18, true);
          public               postgres    false    223            �           0    0 (   операции_id_операции_seq    SEQUENCE SET     Y   SELECT pg_catalog.setval('public."операции_id_операции_seq"', 1, false);
          public               postgres    false    221            �           0    0 >   процентная_став_id_процентной_ст_seq    SEQUENCE SET     n   SELECT pg_catalog.setval('public."процентная_став_id_процентной_ст_seq"', 5, true);
          public               postgres    false    229            �           0    0    роли_id_роли_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public."роли_id_роли_seq"', 3, true);
          public               postgres    false    215            �           0    0    счет_id_счета_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public."счет_id_счета_seq"', 19, true);
          public               postgres    false    231            �           0    0 ,   тип_счета_id_типа_счета_seq    SEQUENCE SET     \   SELECT pg_catalog.setval('public."тип_счета_id_типа_счета_seq"', 1, true);
          public               postgres    false    219            �           0    0    улица_id_улицы_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public."улица_id_улицы_seq"', 3, true);
          public               postgres    false    217            �           0    0 "   филиал_id_филиала_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public."филиал_id_филиала_seq"', 3, true);
          public               postgres    false    225                       2606    24796 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    235                        2606    16784 P   банковская_операция банковская_операция_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."банковская_операция"
    ADD CONSTRAINT "банковская_операция_pkey" PRIMARY KEY ("id_банковской_операции");
 ~   ALTER TABLE ONLY public."банковская_операция" DROP CONSTRAINT "банковская_операция_pkey";
       public                 postgres    false    234            �           2606    16724 (   вид_счета вид_счета_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."вид_счета"
    ADD CONSTRAINT "вид_счета_pkey" PRIMARY KEY ("id_вида_счета");
 V   ALTER TABLE ONLY public."вид_счета" DROP CONSTRAINT "вид_счета_pkey";
       public                 postgres    false    228            �           2606    16698    клиент клиент_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT "клиент_pkey" PRIMARY KEY ("id_клиента");
 L   ALTER TABLE ONLY public."клиент" DROP CONSTRAINT "клиент_pkey";
       public                 postgres    false    224            �           2606    16680 &   операции операции_pkey 
   CONSTRAINT     {   ALTER TABLE ONLY public."операции"
    ADD CONSTRAINT "операции_pkey" PRIMARY KEY ("id_операции");
 T   ALTER TABLE ONLY public."операции" DROP CONSTRAINT "операции_pkey";
       public                 postgres    false    222            �           2606    16736 X   процентная_ставка_в_сч процентная_ставка_в_сч_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."процентная_ставка_в_сч"
    ADD CONSTRAINT "процентная_ставка_в_сч_pkey" PRIMARY KEY ("id_процентной_ставки");
 �   ALTER TABLE ONLY public."процентная_ставка_в_сч" DROP CONSTRAINT "процентная_ставка_в_сч_pkey";
       public                 postgres    false    230            �           2606    16651    роли роли_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public."роли"
    ADD CONSTRAINT "роли_pkey" PRIMARY KEY ("id_роли");
 D   ALTER TABLE ONLY public."роли" DROP CONSTRAINT "роли_pkey";
       public                 postgres    false    216            �           2606    16653    роли роли_роль_key 
   CONSTRAINT     c   ALTER TABLE ONLY public."роли"
    ADD CONSTRAINT "роли_роль_key" UNIQUE ("роль");
 L   ALTER TABLE ONLY public."роли" DROP CONSTRAINT "роли_роль_key";
       public                 postgres    false    216            �           2606    16748    счет счет_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_pkey" PRIMARY KEY ("id_счета");
 D   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_pkey";
       public                 postgres    false    232            �           2606    16671 (   тип_счета тип_счета_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."тип_счета"
    ADD CONSTRAINT "тип_счета_pkey" PRIMARY KEY ("id_типа_счета");
 V   ALTER TABLE ONLY public."тип_счета" DROP CONSTRAINT "тип_счета_pkey";
       public                 postgres    false    220            �           2606    16662    улица улица_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public."улица"
    ADD CONSTRAINT "улица_pkey" PRIMARY KEY ("id_улицы");
 H   ALTER TABLE ONLY public."улица" DROP CONSTRAINT "улица_pkey";
       public                 postgres    false    218            �           2606    16710    филиал филиал_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public."филиал"
    ADD CONSTRAINT "филиал_pkey" PRIMARY KEY ("id_филиала");
 L   ALTER TABLE ONLY public."филиал" DROP CONSTRAINT "филиал_pkey";
       public                 postgres    false    226            �           1259    24797    ix_клиент_email    INDEX     Z   CREATE UNIQUE INDEX "ix_клиент_email" ON public."клиент" USING btree (email);
 +   DROP INDEX public."ix_клиент_email";
       public                 postgres    false    224            �           1259    24798 !   ix_клиент_id_клиента    INDEX     m   CREATE INDEX "ix_клиент_id_клиента" ON public."клиент" USING btree ("id_клиента");
 7   DROP INDEX public."ix_клиент_id_клиента";
       public                 postgres    false    224                       2620    49431 #   клиент trg_check_unique_email    TRIGGER     �   CREATE TRIGGER trg_check_unique_email BEFORE INSERT OR UPDATE ON public."клиент" FOR EACH ROW EXECUTE FUNCTION public.check_unique_email();
 >   DROP TRIGGER trg_check_unique_email ON public."клиент";
       public               postgres    false    224    289            
           2606    16790 d   банковская_операция банковская_операция_id_операции_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."банковская_операция"
    ADD CONSTRAINT "банковская_операция_id_операции_fkey" FOREIGN KEY ("id_операции") REFERENCES public."операции"("id_операции");
 �   ALTER TABLE ONLY public."банковская_операция" DROP CONSTRAINT "банковская_операция_id_операции_fkey";
       public               postgres    false    3314    222    234                       2606    16785 ^   банковская_операция банковская_операция_id_счета_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."банковская_операция"
    ADD CONSTRAINT "банковская_операция_id_счета_fkey" FOREIGN KEY ("id_счета") REFERENCES public."счет"("id_счета");
 �   ALTER TABLE ONLY public."банковская_операция" DROP CONSTRAINT "банковская_операция_id_счета_fkey";
       public               postgres    false    234    3326    232                       2606    16725 ?   вид_счета вид_счета_id_типа_счета_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."вид_счета"
    ADD CONSTRAINT "вид_счета_id_типа_счета_fkey" FOREIGN KEY ("id_типа_счета") REFERENCES public."тип_счета"("id_типа_счета");
 m   ALTER TABLE ONLY public."вид_счета" DROP CONSTRAINT "вид_счета_id_типа_счета_fkey";
       public               postgres    false    228    3312    220                       2606    16699 *   клиент клиент_id_роли_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT "клиент_id_роли_fkey" FOREIGN KEY ("id_роли") REFERENCES public."роли"("id_роли");
 X   ALTER TABLE ONLY public."клиент" DROP CONSTRAINT "клиент_id_роли_fkey";
       public               postgres    false    224    216    3306                       2606    16737 h   процентная_ставка_в_сч процентная_ставка__id_вида_счета_fkey    FK CONSTRAINT        ALTER TABLE ONLY public."процентная_ставка_в_сч"
    ADD CONSTRAINT "процентная_ставка__id_вида_счета_fkey" FOREIGN KEY ("id_вида_счета") REFERENCES public."вид_счета"("id_вида_счета");
 �   ALTER TABLE ONLY public."процентная_ставка_в_сч" DROP CONSTRAINT "процентная_ставка__id_вида_счета_fkey";
       public               postgres    false    230    228    3322                       2606    16759 -   счет счет_id_вида_счета_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_id_вида_счета_fkey" FOREIGN KEY ("id_вида_счета") REFERENCES public."вид_счета"("id_вида_счета");
 [   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_id_вида_счета_fkey";
       public               postgres    false    228    3322    232                       2606    16749 (   счет счет_id_клиента_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_id_клиента_fkey" FOREIGN KEY ("id_клиента") REFERENCES public."клиент"("id_клиента");
 V   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_id_клиента_fkey";
       public               postgres    false    224    232    3318            	           2606    16754 (   счет счет_id_филиала_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."счет"
    ADD CONSTRAINT "счет_id_филиала_fkey" FOREIGN KEY ("id_филиала") REFERENCES public."филиал"("id_филиала");
 V   ALTER TABLE ONLY public."счет" DROP CONSTRAINT "счет_id_филиала_fkey";
       public               postgres    false    226    232    3320                       2606    16711 8   филиал филиал_улица_филиала_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."филиал"
    ADD CONSTRAINT "филиал_улица_филиала_fkey" FOREIGN KEY ("улица_филиала") REFERENCES public."улица"("id_улицы");
 f   ALTER TABLE ONLY public."филиал" DROP CONSTRAINT "филиал_улица_филиала_fkey";
       public               postgres    false    226    3310    218            �           3256    32991 $   клиент client_isolation_policy    POLICY     �   CREATE POLICY client_isolation_policy ON public."клиент" USING (("id_клиента" = (current_setting('app.current_client_id'::text, true))::integer));
 >   DROP POLICY client_isolation_policy ON public."клиент";
       public               postgres    false    224    224            �           3256    50026    клиент client_rls_policy    POLICY     �   CREATE POLICY client_rls_policy ON public."клиент" FOR SELECT USING (((email)::text = current_setting('app.current_email'::text, true)));
 8   DROP POLICY client_rls_policy ON public."клиент";
       public               postgres    false    224    224            �           3256    49434 "   клиент operator_access_hours    POLICY     `  CREATE POLICY operator_access_hours ON public."клиент" FOR SELECT USING ((((current_setting('app.current_role_id'::text, true))::integer <> 3) OR ((date_part('hour'::text, (now() AT TIME ZONE 'Europe/Moscow'::text)) >= (9)::double precision) AND (date_part('hour'::text, (now() AT TIME ZONE 'Europe/Moscow'::text)) <= (18)::double precision))));
 <   DROP POLICY operator_access_hours ON public."клиент";
       public               postgres    false    224            �           3256    49441 #   клиент operator_access_policy    POLICY     %  CREATE POLICY operator_access_policy ON public."клиент" FOR SELECT USING (((current_setting('app.current_email'::text, true) = (email)::text) AND (EXISTS ( SELECT 1
   FROM public.operator_info
  WHERE (((operator_info.email)::text = current_setting('app.current_email'::text, true)) AND (operator_info."id_роли" = 3) AND ((date_part('hour'::text, (CURRENT_TIME AT TIME ZONE 'Europe/Moscow'::text)) >= (9)::double precision) AND (date_part('hour'::text, (CURRENT_TIME AT TIME ZONE 'Europe/Moscow'::text)) <= (18)::double precision)))))));
 =   DROP POLICY operator_access_policy ON public."клиент";
       public               postgres    false    236    224    236    224            �           3256    41186    клиент user_access_policy    POLICY     m   CREATE POLICY user_access_policy ON public."клиент" FOR SELECT USING ((CURRENT_USER = (email)::text));
 9   DROP POLICY user_access_policy ON public."клиент";
       public               postgres    false    224    224            �           0    16691    клиент    ROW SECURITY     <   ALTER TABLE public."клиент" ENABLE ROW LEVEL SECURITY;          public               postgres    false    224            �           3256    49433 >   клиент оператор_доступ_по_времени    POLICY     B  CREATE POLICY "оператор_доступ_по_времени" ON public."клиент" FOR SELECT USING ((((current_setting('app.current_role_id'::text, true))::integer <> 3) OR ((date_part('hour'::text, CURRENT_TIME) >= (9)::double precision) AND (date_part('hour'::text, CURRENT_TIME) <= (17)::double precision))));
 Z   DROP POLICY "оператор_доступ_по_времени" ON public."клиент";
       public               postgres    false    224            �      x��01JM4M51K�4����� +K�      �   �   x����C1��g�,�C��Y��MZ���J���O�r���b��B[BӸ��v%]q�JNՓ�y�Q�(�*��F���j}�����wՏy����-�\��=�F��a�E����٦�aA��쿒]&��Yx�Dj4������==DC�      �   �   x�e�=�@��Sp�a
),L���`@DX�����L�/��vS��9'`�X�P$��F�A��	*�ZlaKD?b�@f��Ѓ�;C������n_;�|qd�J�[��L�"�����������#���1Y�H�3�t�P�܈0      �   B  x���ˎ���Ǯ������{s��}l�f0�d�����Q+�3�ԓV�7h%)�;��3��Qpչ�I���r$$X��k}�ׂLǏ�$����(�cչ���������o׿_�\��Ri���� "���"��=@� �8 ���w�!�D�r�iV;Ev�ȉN�<K	�N{ �
3ڦ�dښ`�c�Z��H�:�y�s9/�é`\(�B!$*�J�g�r8e�����n/�.��\��)�)�p��#�����C9�޿��
�ф��l��$a�pm�����`Dxs���n�w/�w�8!Ũ���&�f:�sɛ�g|�Z�.5�L�؅��H2�`c�A�)���n{p���C������^{�����W����� ��"�P=���zM�9�V;��ҏ�3����|.�@�í��$3��7V�Ţ�M��>�o��-	(ܦ\�q1?H������Q��t���,K�x����P�^?�譳��[�N�(�2��
���G"���j��r���D�4Mƃ�i.C�5�a:�y���3N����g���9d����[�S��xq�� ��۬�d��1��I��L���
o!E}&h-�h5>+����ف{������8^0<@��R�LM�g�L@�k��ʄ���
��6�m�!JO��hċ�޷x�`
�W� Fٲ��nl�-�f4�&�	a�x{�.��|/���(z�+�������G�N�a]"�s��h�(��f6�*��;;�_�z}�=��'��>����D~(^�~��I�H� "p�5�K9@��ԉRUqL�y���3���a����8�&�~����I�B��7���-��β����
�����#�,F)[ ��J���R=���`�IϦ+�hF�9w&Q|u�����R�<�gv<��*^g�~���9H�V�� bY,��h���͕��4v�z�>|9kl'�Z~���|�������ҿ��^�=�=@��1β�5���(��z)���_�Q�F`ʴ����V`��������*m��f�����c���M�M�ޞ�6�;�l~'-
j'..��MK�]�ݠ�.M�>��Ħ��)`9��"*�e�
��y�z��H����i[qxߣ�km�|-/'kO5~^�L椳5��i�)�)����>}l3������>�X����.d�!�C�G"��e^�>mT�58E5��_d:d�$`J]񙹨�9D ��1f4CC�=_�o��Ŷ��+��CvWPJ v�X��S�Q�Hga�0`&j:l�݄ONB�4���-��2k<Y��l}�f��{ ��m#�r��n������*�6��zw�����/	�`      �   <   x�3�0�¾��x�����[��8/,���b��&0��j����&��-\1z\\\ �l#�      �   h   x�e��A�w;�M`Gnc�c!�8 	� ��E�0��5n�KsT���.�'��E��X�,�8� ���x�&�=��hJ���Y�\�vK������t�c��\K�      �   ?   x�4 ��1	клиент
2	админ
3	оператор
\.


F��      �     x�]�ˍ1D��QL;�d�2��bp��z}��*����\0.���5N��8y3
�^�ϯ�n��E���c����dB�E�-�甚�H��Ǣ6���.�H�/�g����� �V����՗�rZ�=wC.�n\���6NƠ�E��R v���D���I$ �I����i�.מ2҈P���9.9�J�s�����"*S��o���E��k�3�tP������z��&�)�7��]^g=�;��3G�� ���}��o��ga      �   _   x�%��� �ϼ)��ğq9x��*�@�p�v#���~�:Z$Dd:Tz�2\(xe1Ȩ
w52�MIwW��7����j�9h�t���"�LiB�      �   Q   x�Ƚ	�0F�:o
'��8L��`aag�Q	��;�o#S��o*^�b�ƣ��]A���Uwᤑ�A�α�8I
\|����~�%))      �      x�3�4�44�4�2�4�46�4����� #��     