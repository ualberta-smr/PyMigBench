# Copyright (c) 2010, individual contributors (see AUTHORS file)
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from PIL import Image
import os
from django.db import models
from settings import SCREENSHOT_URL, SCREENSHOT_PATH
from Project import Project

SCREENSHOT_WIDTH = 230.0
SCREENSHOT_HEIGHT = 170.0

MAIN_PAGE_WIDTH = 605.0
MAIN_PAGE_HEIGHT = 300.0

# a screenshot for a project, display on its page. its filename is derived from
# its ID, so it is not required as a field
class Screenshot(models.Model):
  class Meta:
    app_label = 'dashboard'
  
  # the title of the screenshot
  title = models.CharField(max_length = 32)

  # a short description of the screenshot
  description = models.CharField(max_length = 100)
  
  # what project is this a screenshot of?
  project = models.ForeignKey(Project)
  
  # file extension
  extension = models.CharField(max_length = 8)
  
  # save override to validate title/description length
  def save(self, *args, **kwargs):
    self.title = self.title[0:32]
    self.description = self.description[0:100]
    super(Screenshot, self).save(*args, **kwargs)
  
  # the filename for this file. just the last part, no directory specified.
  def filename(self):
    return "{0}{1}".format(str(self.id), self.extension)
  
  # the thumbnail filename for this file, no directory specified.
  def thumbnail(self):
    return str(self.id) + "_t.png"
  
  # the url of a screenshot
  def url(self):
    return os.path.join(SCREENSHOT_URL, self.filename())
  
  # the thumbnail url of a screenshot
  def thumb_url(self):
    return os.path.join(SCREENSHOT_URL, self.thumbnail())
  
  # the large thumbnail to be used on the main page
  def main_page_url(self):
    return os.path.join(SCREENSHOT_URL, str(self.id) + "_mp.png")
  
  # a static creation method to handle writing to disk
  @staticmethod
  def create(form, file, project):
    # create a screenshot object in the database
    screen = Screenshot(title = form.cleaned_data["title"],
                        description = form.cleaned_data["description"],
                        project = project,
                        extension = os.path.splitext(file.name)[1])
    screen.save()
    
    # write the screenshot to a file
    path = os.path.join(SCREENSHOT_PATH, screen.filename())
    write = open(path, 'wb+')
    
    # write the chunks
    for chunk in file.chunks():
      write.write(chunk)
    write.close()
    
    def create_thumbnail(path, save, width, height):
      # create a thumbnail of the file
      img = Image.open(path)
      
      # resize the image for a thumbnail
      scalex = width / img.size[0]
      scaley = height / img.size[1]
      scale = scalex if scalex > scaley else scaley
      img = img.resize((int(img.size[0] * scale),
                        int(img.size[1] * scale)),
                       Image.ANTIALIAS)
      
      # crop the image to fit
      if img.size[0] > width or img.size[1] > height:
        left = (img.size[0] - width) / 2
        right = left + width
        top = (img.size[1] - height) / 2
        bottom = top + height
        img = img.crop((int(left), int(top), int(right), int(bottom)))
      
      # save the thumbnail
      save_path = os.path.join(SCREENSHOT_PATH, save.format(str(screen.id)))
      img.save(save_path, "PNG")
    
    create_thumbnail(path, "{0}_t.png", SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)
    create_thumbnail(path, "{0}_mp.png", MAIN_PAGE_WIDTH, MAIN_PAGE_HEIGHT)
    
    return screen

