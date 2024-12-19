-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 19 Des 2024 pada 18.40
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_booking`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_ruang`
--

CREATE TABLE `detail_ruang` (
  `id_ruang` int(11) NOT NULL,
  `img` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_admin`
--

CREATE TABLE `tb_admin` (
  `id_admin` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_admin`
--

INSERT INTO `tb_admin` (`id_admin`, `username`, `password`) VALUES
(1, 'Abdul Hijjah Jomok', '123123'),
(2, 'Muhammad Faris Wafda', '123123');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_form`
--

CREATE TABLE `tb_form` (
  `id_form` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `nim` bigint(50) NOT NULL,
  `nama_peminjam` varchar(255) NOT NULL,
  `id_ruang` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `perihal` longtext NOT NULL,
  `proposal` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `id_admin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_form`
--

INSERT INTO `tb_form` (`id_form`, `id_user`, `nim`, `nama_peminjam`, `id_ruang`, `start_date`, `end_date`, `perihal`, `proposal`, `status`, `id_admin`) VALUES
(28, 3, 123, 'as', 4, '2024-12-20', '2024-12-21', '123', 'Review_Jurnal_Resnet50.pdf', 'Diterima', 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_ruang`
--

CREATE TABLE `tb_ruang` (
  `id_ruang` int(11) NOT NULL,
  `nama_ruang` varchar(255) NOT NULL,
  `kapasitas` int(11) NOT NULL,
  `deskripsi` longtext NOT NULL,
  `iframe` longtext NOT NULL,
  `fasilitas` longtext NOT NULL,
  `img` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_ruang`
--

INSERT INTO `tb_ruang` (`id_ruang`, `nama_ruang`, `kapasitas`, `deskripsi`, `iframe`, `fasilitas`, `img`) VALUES
(1, 'Audit Mini', 20, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In orci felis, porta et lacinia non, fermentum eu enim. Maecenas consectetur velit sem, et suscipit libero hendrerit eget. Proin posuere aliquam egestas. Donec pellentesque ac turpis at consectetur. Praesent tempor ligula id dolor ultrices suscipit ac non justo.', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d588.5034271297164!2d112.72458391423055!3d-7.130232968231368!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd803dc583cdd09%3A0x9acf1238119304fc!2sFakultas%20Teknik%20-%20UTM!5e0!3m2!1sid!2sid!4v1734541753166!5m2!1sid!2sid', '6 AC, Wifi Gratis, Proyektor, Kursi dan Meja Lengkap, Sound System, Parkir Luas', 'auditmini.jpg'),
(2, 'F409', 40, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In orci felis, porta et lacinia non, fermentum eu enim. Maecenas consectetur velit sem, et suscipit libero hendrerit eget. Proin posuere aliquam egestas. Donec pellentesque ac turpis at consectetur. Praesent tempor ligula id dolor ultrices suscipit ac non justo.', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d588.5034271297164!2d112.72458391423055!3d-7.130232968231368!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd803dc583cdd09%3A0x9acf1238119304fc!2sFakultas%20Teknik%20-%20UTM!5e0!3m2!1sid!2sid!4v1734541753166!5m2!1sid!2sid', '40 Bangku, Proyektor, Papan Tulis, 2 AC, Tempat Charger', 'f409.jpg'),
(3, 'Lab Sistem Terdistribusi', 40, 'Lab Yang Cocok untuk mengerjakan tugas bersama dan juga dapat bermain game bersama', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d294.25257071349466!2d112.72557190428668!3d-7.1288986204806175!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd803dd17f71c6b%3A0x27ada1058b509ced!2sLaboratorium%20Teknologi%20Informasi%20dan%20Aplikasi%20(Lab%20TIA)%2C%20Universitas%20Trunojoyo%20Madura%20-%20UTM!5e0!3m2!1sid!2sid!4v1734610336816!5m2!1sid!2sid\" ', 'Internet (LAN) up to 100MBps, Meja Kursi Komplit, 2 AC, Refill Air Mineral, Monitor, Tempat Charger', 'sister.jpg'),
(4, 'Lab Riset', 40, 'Lab untuk riset penelitian, kerjasama tim, dapat dipakai untuk mabar', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d294.25257071349466!2d112.72557190428668!3d-7.1288986204806175!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd803dd17f71c6b%3A0x27ada1058b509ced!2sLaboratorium%20Teknologi%20Informasi%20dan%20Aplikasi%20(Lab%20TIA)%2C%20Universitas%20Trunojoyo%20Madura%20-%20UTM!5e0!3m2!1sid!2sid!4v1734610336816!5m2!1sid!2sid\"', 'Internet (LAN) up to 150MBps, Meja Kursi Komplit, 2 AC, Refill Air Mineral, Monitor, Tempat Charger', 'riset.jpg'),
(5, 'Lab Common Computing', 45, 'Lab dengan fasilitas komputer terbaik, cocok untuk riset penelitian yang membutuhkan performa komputer yang mumpuni, AC dingin', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d294.25257071349466!2d112.72557190428668!3d-7.1288986204806175!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd803dd17f71c6b%3A0x27ada1058b509ced!2sLaboratorium%20Teknologi%20Informasi%20dan%20Aplikasi%20(Lab%20TIA)%2C%20Universitas%20Trunojoyo%20Madura%20-%20UTM!5e0!3m2!1sid!2sid!4v1734610336816!5m2!1sid!2sid\" ', 'Komputer I7 Gen 14, Proyektor, Papan Tulis, Meja Kursi Lengkap, 4 AC, Monitor Cakep', 'cc.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_users`
--

CREATE TABLE `tb_users` (
  `id_user` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_users`
--

INSERT INTO `tb_users` (`id_user`, `username`, `email`, `password`) VALUES
(1, 'faris wafda', 'tes@gmail.com', 'scrypt:32768:8:1$3G8kPPA5jMXipxeH$4871b7bc197a55d95f63c2a092cc66f0582df14dac5eb47d159ea5a4e33d0a39b6c6456730000e2e219f9b729a5ad81b9b717a9e43635497f70fee1c068d93ea'),
(2, 'wafda', 'wafda@gmail.com', 'scrypt:32768:8:1$obuE5CBMckg1DiyL$ba88aa54d6d5f4133d284d9323f16f2a24821039fd04717721567375c8fe36a9bfc3e6fe7595a57a9953caecedee162397a6a00c622ea222abf566ecff7b1541'),
(3, 'akbar', 'akbar@gmail.com', 'scrypt:32768:8:1$IDE6BQYNJWNSeUQc$69a9d5656b62b7145ffaa73ef53b9f41645d5d67662f6387a50f1d37fa60a20c019a29ead4832c72114f811283d68803230389f5f6f614dd8f69e3b879fa9e18'),
(9, 'admin', 'admin@gmail.com', 'scrypt:32768:8:1$32NSNtnB8SUrKpDN$bfcbfdf90d0ae8ee11a5bc19ec724690b590bf302edb5abd3bda71a7d44e4e3aa0d46a605b72e346833f7b45865bc7180edf08d33430508a12acd715cc832b61'),
(10, 'cobaa', 'coba@gmail.com', 'scrypt:32768:8:1$3MaZ0c2vHQU7X8HJ$655219971b9325bc83ef9dec8f7826ad9f9468e2ed04175b63c4cb4f09d829fffd40c8b4c4e12ed68c719459da2e1afc951f24efd0cc3e27520234eefac9aeca');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `detail_ruang`
--
ALTER TABLE `detail_ruang`
  ADD KEY `id_ruang` (`id_ruang`);

--
-- Indeks untuk tabel `tb_admin`
--
ALTER TABLE `tb_admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indeks untuk tabel `tb_form`
--
ALTER TABLE `tb_form`
  ADD PRIMARY KEY (`id_form`),
  ADD KEY `id_ruang` (`id_ruang`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_admin` (`id_admin`);

--
-- Indeks untuk tabel `tb_ruang`
--
ALTER TABLE `tb_ruang`
  ADD PRIMARY KEY (`id_ruang`);

--
-- Indeks untuk tabel `tb_users`
--
ALTER TABLE `tb_users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tb_admin`
--
ALTER TABLE `tb_admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `tb_form`
--
ALTER TABLE `tb_form`
  MODIFY `id_form` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT untuk tabel `tb_ruang`
--
ALTER TABLE `tb_ruang`
  MODIFY `id_ruang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `tb_users`
--
ALTER TABLE `tb_users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `detail_ruang`
--
ALTER TABLE `detail_ruang`
  ADD CONSTRAINT `detail_ruang_ibfk_1` FOREIGN KEY (`id_ruang`) REFERENCES `tb_ruang` (`id_ruang`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tb_form`
--
ALTER TABLE `tb_form`
  ADD CONSTRAINT `tb_form_ibfk_1` FOREIGN KEY (`id_ruang`) REFERENCES `tb_ruang` (`id_ruang`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tb_form_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `tb_users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tb_form_ibfk_3` FOREIGN KEY (`id_admin`) REFERENCES `tb_admin` (`id_admin`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
