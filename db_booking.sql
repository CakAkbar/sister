-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 18 Des 2024 pada 08.50
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
-- Struktur dari tabel `tb_form`
--

CREATE TABLE `tb_form` (
  `id_form` int(11) NOT NULL,
  `nama_peminjam` varchar(255) NOT NULL,
  `id_ruang` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `proposal` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_form`
--

INSERT INTO `tb_form` (`id_form`, `nama_peminjam`, `id_ruang`, `start_date`, `end_date`, `proposal`) VALUES
(1, 'Wafda', 1, '2024-12-18', '2024-12-20', 'uploads\\Review_Jurnal_Resnet50.docx'),
(2, 'faris', 2, '2024-12-20', '2024-12-21', 'uploads\\draft_proposal.docx'),
(3, 'akbar', 2, '2024-12-22', '2024-12-24', 'uploads\\jgn_resubmit_sampe_tgl_10_jam_2_siang.docx'),
(4, 'aa', 1, '2024-12-21', '2024-12-22', 'uploads\\Review_Jurnal_Resnet50.docx'),
(5, 'bb', 1, '2024-12-23', '2024-12-25', 'uploads\\Review_Jurnal_Resnet50.docx'),
(6, 'cc', 1, '2024-12-26', '2024-12-31', 'uploads\\Review_Jurnal_Resnet50.docx'),
(7, 'dd', 1, '2025-01-01', '2025-01-03', 'uploads\\Review_Jurnal_Resnet50.docx'),
(8, 'Wafda', 2, '2024-12-25', '2024-12-26', 'uploads\\Review_Jurnal_Resnet50.docx'),
(9, 'bara ilham', 2, '2024-12-27', '2024-12-28', 'uploads\\Review_Jurnal_Resnet50.docx'),
(10, 'asdw', 2, '2024-12-29', '2024-12-30', 'uploads\\Review_Jurnal_Resnet50.docx'),
(11, 'ww', 2, '2024-12-31', '2025-01-01', 'uploads\\Review_Jurnal_Resnet50.docx'),
(12, 'gfg', 2, '2025-01-02', '2025-01-03', 'uploads\\Review_Jurnal_Resnet50.docx'),
(13, 'agafsdf', 1, '2025-01-04', '2025-01-04', 'uploads\\Review_Jurnal_Resnet50.docx'),
(15, 'aqqww', 1, '2025-01-05', '2025-01-05', 'uploads\\Review_Jurnal_Resnet50.docx'),
(16, 'sethe', 1, '2025-01-07', '2025-01-09', 'uploads\\Review_Jurnal_Resnet50.docx');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_ruang`
--

CREATE TABLE `tb_ruang` (
  `id_ruang` int(11) NOT NULL,
  `nama_ruang` varchar(255) NOT NULL,
  `kapasitas` int(11) NOT NULL,
  `deskripsi` longtext NOT NULL,
  `lokasi` varchar(255) NOT NULL,
  `fasilitas` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_ruang`
--

INSERT INTO `tb_ruang` (`id_ruang`, `nama_ruang`, `kapasitas`, `deskripsi`, `lokasi`, `fasilitas`) VALUES
(1, 'Audit Mini', 20, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In orci felis, porta et lacinia non, fermentum eu enim. Maecenas consectetur velit sem, et suscipit libero hendrerit eget. Proin posuere aliquam egestas. Donec pellentesque ac turpis at consectetur. Praesent tempor ligula id dolor ultrices suscipit ac non justo.', '', '6 AC, Wifi Gratis, Proyektor, Kursi dan Meja Lengkap, Sound System, Parkir Luas, Free Refill Air Mineral'),
(2, 'F409', 40, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In orci felis, porta et lacinia non, fermentum eu enim. Maecenas consectetur velit sem, et suscipit libero hendrerit eget. Proin posuere aliquam egestas. Donec pellentesque ac turpis at consectetur. Praesent tempor ligula id dolor ultrices suscipit ac non justo.', '', '');

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
(1, 'faris wafda', 'tes@gmail.com', 'scrypt:32768:8:1$3G8kPPA5jMXipxeH$4871b7bc197a55d95f63c2a092cc66f0582df14dac5eb47d159ea5a4e33d0a39b6c6456730000e2e219f9b729a5ad81b9b717a9e43635497f70fee1c068d93ea');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `detail_ruang`
--
ALTER TABLE `detail_ruang`
  ADD KEY `id_ruang` (`id_ruang`);

--
-- Indeks untuk tabel `tb_form`
--
ALTER TABLE `tb_form`
  ADD PRIMARY KEY (`id_form`),
  ADD KEY `id_ruang` (`id_ruang`);

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
-- AUTO_INCREMENT untuk tabel `tb_form`
--
ALTER TABLE `tb_form`
  MODIFY `id_form` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT untuk tabel `tb_ruang`
--
ALTER TABLE `tb_ruang`
  MODIFY `id_ruang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `tb_users`
--
ALTER TABLE `tb_users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  ADD CONSTRAINT `tb_form_ibfk_1` FOREIGN KEY (`id_ruang`) REFERENCES `tb_ruang` (`id_ruang`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
