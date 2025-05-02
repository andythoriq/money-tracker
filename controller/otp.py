import random
import os
import smtplib
import time
from email.message import EmailMessage
from dotenv import load_dotenv


class Otp:
    def __init__(self):
        self.last_otp_time = 0
        self.cooldown_duration = 60  # 1 menit dalam detik
        self.current_otp = ""
        self.otp_expiry = 0

    def is_cooldown_active(self):
        current_time = time.time()
        if current_time - self.last_otp_time < self.cooldown_duration:
            remaining_time = int(
                self.cooldown_duration - (current_time - self.last_otp_time)
            )
            return True, remaining_time
        return False, 0

    def is_otp_expired(self):
        current_time = time.time()
        if current_time > self.otp_expiry:
            return True
        return False

    def startsmtp(self, usermail, key_dict):
        cooldown_active, remaining_time = self.is_cooldown_active()
        if cooldown_active:
            print(f"Harap tunggu {remaining_time} detik sebelum mengirim OTP lagi")
            return False

        load_dotenv()
        self.current_otp = ""
        print("Loading...")
        for _ in range(6):
            self.current_otp += str(random.randint(0, 9))

        sender = "noreply31315@gmail.com"
        AUTHKEY = os.getenv("AUTHKEY")

        try:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login(sender, str(AUTHKEY))
            receiver = usermail

            otpmsg = EmailMessage()
            otpmsg["Subject"] = "Kode OTP Aplikasi Money Tracker"
            otpmsg["From"] = sender
            otpmsg["To"] = receiver
            otpmsg.set_content(
                f"Kode OTP anda adalah {self.current_otp} \nJANGAN BAGIKAN KODE OTP DENGAN SIAPAPUN! \nsilahkan masukan kode ke aplikasi Money Tracker"
            )

            smtp.send_message(otpmsg)
            print("Kode OTP Terkirim (Harap Cek Folder Spam Didalam Email Anda!)")
            smtp.quit()

            self.last_otp_time = time.time()
            self.otp_expiry = self.last_otp_time + 300  # OTP berlaku selama 5 menit
            key_dict["key"] = self.current_otp
            return True
        except Exception as e:
            import traceback
            print("Terjadi kesalahan:")
            traceback.print_exc()            
            return False

    def otpcheck(self, userotp, otpcode):
        if self.is_otp_expired():
            print("Kode OTP sudah kadaluarsa! Silakan minta kode baru.")
            return False

        if not userotp or not otpcode:
            print("Kode OTP tidak valid!")
            return False

        if userotp == otpcode:
            print("Kode OTP Benar!")
            return True
        else:
            print("Kode OTP Salah!")
            return False