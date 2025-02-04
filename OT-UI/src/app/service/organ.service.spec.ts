import { TestBed } from '@angular/core/testing';

import { OrganService } from './organ.service';

describe('OrganService', () => {
  let service: OrganService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(OrganService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
