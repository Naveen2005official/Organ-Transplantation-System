import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OrganService } from './service/organ.service';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  recipientData = {
    Recipient_Age: 30,
    Recipient_Gender: "Male",
    Recipient_Blood_Type: "O+",
    Organ_Type_Needed: "Kidney",
    Priority_Level: 2,
    Wait_Time_Months: 12
  };

  bestDonor: any = null;

  constructor(private organService: OrganService) {}

  findDonor() {
    this.organService.getBestDonor(this.recipientData).subscribe({
      next: (response) => {
        this.bestDonor = response;
      },
      error: (error) => {
        console.error("Error fetching donor", error);
      }
    });

  }
}
