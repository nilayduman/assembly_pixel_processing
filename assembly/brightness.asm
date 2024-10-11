section .data
    file_name db 'pixels.bin', 0
    output_file db 'output_pixels.bin', 0
    buffer times 1024 db 0   ; Piksellerin okunduğu tampon bellek

section .bss
    file_descriptor resd 1
    num_bytes resd 1

section .text
    global _start

_start:
    ; Görüntü dosyasını aç
    mov eax, 5          ; sys_open
    mov ebx, file_name  ; dosya adı
    mov ecx, 0          ; sadece okuma
    int 0x80

    ; Dosya tanımlayıcısını kaydet
    mov [file_descriptor], eax

    ; Pikselleri oku
    mov eax, 3          ; sys_read
    mov ebx, [file_descriptor]
    mov ecx, buffer     ; buffer'a pikselleri oku
    mov edx, 1024       ; 1024 byte oku
    int 0x80

    ; Basit parlaklık arttırma (her pikselin değerini 10 artır)
    mov ecx, 1024       ; kaç piksel olduğunu belirle
    xor ebx, ebx        ; başlangıç indeksi
loop_start:
    mov al, [buffer + ebx]  ; bir piksel oku
    add al, 10              ; parlaklığı 10 artır
    mov [buffer + ebx], al  ; yeni değeri yaz
    inc ebx
    loop loop_start

    ; Yeni görüntü piksellerini dosyaya yaz
    mov eax, 8          ; sys_creat
    mov ebx, output_file
    mov ecx, 0666       ; dosya izinleri
    int 0x80

    ; Dosyaya yaz
    mov eax, 4          ; sys_write
    mov ebx, [file_descriptor]
    mov ecx, buffer     ; buffer'dan pikselleri al
    mov edx, 1024       ; 1024 byte yaz
    int 0x80

    ; Programı sonlandır
    mov eax, 1          ; sys_exit
    xor ebx, ebx
    int 0x80
